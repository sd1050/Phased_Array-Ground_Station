#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
import numpy
import pycuda.compiler
import pycuda.driver

class Cuda_MVDR_Beamforming(gr.decim_block):
    """
    - Block instatiates a Cuda kernel for use with a Minimum Variance Distorionless Response (MVDR) Beamformer
    - Targeted use is a 2x2 planar array connected to a Nvidia Jetson Nano
    - Built from a decimation block to achieve 4:1 Input/Output relationship
    All CUDA resources (i.e., device context, compiled kernel code, pointers to device memory, etc.) are managed within this block.
    CUDA related code and resource management is inspired from the gr-CUDA block developed by Deepwave Digital (deepwavedigital.com) 
    """
    def __init__(self, device_num, io_type, vlen, threads_per_block):
        gr.decim_block.__init__(self,
            name="Cuda_MVDR_Beamforming",
            in_sig=[(io_type, vlen)],
            out_sig= [(io_type, vlen)]
        # awaken the GPU
        pycuda.driver.init()
        device = pycuda.driver.Device(device_num)
        # TODO: the following line may need edits
        context_flag = (pycuda.driver.ctx_flags.SCHED_AUTO | pycuda.driver.ctx_flags.MAP_HOST)
        self.context = device.make_context(context_flags)

        # build kernel 
        compiled_cuda = pycuda.compiler.compile("""
        // Going to write kernel here that does some math function to be optimized
        """)
        # alternatively, import a compiled CUDA kernal with pycuda.driver.module_from_file()
        module = pycuda.driver.module_from_buffer(compiled_cuda)

        # extract kernel function from compiled code
        self.kernel = module.get_function("""Retrieve function""").prepare(["dtype", "dtype", "dtype"])
        # keep track of threads are in block
        self.threads_per_block = threads_per_block 

        # Allocate device mapped pinned memory
        self.sample_type = io_type
        self.mapped_host_malloc(vlen)
        self.context.pop()

    def mapped_host_malloc(self, num_samples):
        self.mapped_host_input = \
            pycuda.driver.pagelocked_zeros(
                num_samples,
                self.sample_type,
                mem_flags = pycuda.driver.host_alloc_flags.DEVICEMAP)
        self.mapped_host_output = \
            pycuda.driver.pagelocked_zeros(
                num_samples,
                self.sample_type,
                mem_flags = pycuda.driver.host_alloc_flags.DEVICEMAP)
        self.mapped_gpu_input = self.mapped_host_input.base.get_device_pointer()
        self.mapped_gpu_output = self.mapped_host_output.base.get_device_pointer()
        
        # saves number of samples in an instance, kernel operates on 32-bit fp values so we have x2 option
        self.num_samples = num_samples;
        self.num_floats = self.num_samples;
        if (self.sample_type == numpy.complex64):
            # If we're processing complex data, we have two floats for every sample...
            self.num_floats *= 2
     
        # this segment computes grid and block dimensions for CUDA kernel (1D)
        self.num_blocks = self.num_floats / self.threads_per_block
        left_over_samples = self.num_floats % self.threads_per_block
        if (left_over_samples != 0):
            # If vector length is not an even multiple of the number of threads in a
            # block, we need to add another block to process the "leftover" samples.
            self.num_blocks += 1

    # allows code to recover from unexpected memory situations
    def mapped_host_realloc(self, num_samples):
        del self.mapped_host_input
        del self.mapped_host_output
        self.mapped_host_malloc(num_samples)

    def work(self, input_items, output_items):
        # input_item[0] refers to data on input #1, etc.
        in0 = input_items[0]
        in1 = input_items[1]
        in2 = input_items[2]
        in3 = input_items[3]

        out = output_items[0]
        # taking the sum of samples and vectors received from each port
        recv_vectors = in0.shape[0] + in1.shape[0] + in2.shape[0] + in3.shape[0]
        recv_samples = in0.shape[1] + in1.shape[1] + in2.shape[1] + in3.shape[1]
        self.context.push()
        # prevent self-destruction of memory allocation
        if (recv_samples > self.num_samples):
            print "Warning: Not Enough GPU Memory Allocated. Reallocating..."
            print "-> Required Space: %d Samples" % recv_samples
            print "-> Allocated Space: %d Samples" % self.num_samples
            self.mapped_host_realloc(recv_samples)
        for i in range(0, recv_vectors):
        self.mapped_host_input[0:recv_samples] = in0[i, 0:recv_samples]
        self.kernel.prepared_call((self.num_blocks, 1, 1),
                                    (self.threads_per_block, 1, 1),
                                    self.mapped_gpu_input,
                                    self.mapped_gpu_output,
                                    self.num_floats)
        self.context.synchronize()
        out[i, 0:recv_samples] = self.mapped_host_output[0:recv_samples]
        self.context.pop()
        return recv_vectors
        
        # out[:] = in0
        # return len(output_items[0])

