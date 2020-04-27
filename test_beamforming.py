
import pexpect
import time
import numpy as np
import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import argrelextrema
import warnings
warnings.filterwarnings('ignore')

import pmt
from gnuradio.blocks import parse_file_metadata

def try_flowgraph_expect(testapp, timeout=20):
    try:
        testapp.expect("Press Enter to quit", timeout=timeout)
    except Exception as error:
        if isinstance(error, pexpect.TIMEOUT):
            print ("Timed out before flowgraph finished. Killing process...")
            testapp.sendcontrol("c")
            testapp.close()
        raise error

def try_eof_expect(testapp, timeout=30):
    try:
        testapp.expect([pexpect.EOF], timeout=timeout)
    except Exception as error:
        if isinstance(error, pexpect.TIMEOUT):
            print ("Timed out before finding pexpect EOF. Killing process...")
            testapp.sendcontrol("c")
            testapp.close()
        raise error

def read_binary_iq(filename, **kwargs):
    data = np.fromfile(filename, dtype=np.int16, **kwargs)
    dataiq = (data[::2] + data[1::2]*1j).astype(np.complex)*2**-15
    return dataiq

def signaltonoise(a, axis, ddof): 
    a = np.asanyarray(a) 
    m = a.mean(axis) 
    sd = a.std(axis = axis, ddof = ddof) 
    return np.where(sd == 0, 0, m / sd) 

# Steering Vector Function
def gen_steering_vectors(array_alignment_x, array_alignment_y, thetas, phis):
    M_x = np.size(array_alignment_x, 0)  # Number of antenna elements in x
    M_y = np.size(array_alignment_y,0) # Number of antenna elements in y
    steering_vectors = np.zeros((M_x, M_y,  np.size(thetas), np.size(phis)), dtype=complex) # Creates square matrix at each angle and phi
    for i in range(np.size(thetas)): 
        for j in range(np.size(phis)):
            u = np.cos(np.radians(phis[j]))*np.sin(np.radians(thetas[i])) # Phase propagation change in x direction
            v = np.sin(np.radians(phis[j]))*np.sin(np.radians(thetas[i])) # Phase propagation change in y direction
            x_steering = np.exp(array_alignment_x*(-2j)*np.pi*u)
            x_steering = np.reshape(x_steering, [2,1])
            y_steering = np.exp(array_alignment_y*(-2j)*np.pi*v)
            y_steering = np.reshape(y_steering, [2,1])
            steering_vectors[:,:,i,j] = x_steering*y_steering.T
            #steering_vectors[:,:,i,j] = np.kron(x_steering,y_steering.T)
    steering_vectors = np.reshape(steering_vectors, [4,1,np.size(thetas),np.size(phis)])
    # This makes it a vertical array, from [a b; c d] to [a; b; c; d]. So left to right on top, then left to right on bottom
    return steering_vectors

# DoA Estimation Function
def DoA_MVDR(rx,steering_vectors,incident_thetas, incident_phis):
    R = np.corrcoef(rx)
    #R = forward_backward_avg(R)
    #R = spatial_smoothing(rx.T,4,direction = "forward-backward")
    R_inv  = np.linalg.inv(R) # invert the cross correlation matrix
    ADSINR = np.zeros((np.size(incident_thetas), np.size(incident_phis)))
    for i in range(np.size(incident_thetas)):
        for j in range(np.size(incident_phis)):
            S_theta = steering_vectors[:,:,i,j]
            ADSINR[i,j] = np.dot(np.matrix(S_theta).H,np.dot(R_inv,S_theta))[0,0]
    ADSINR = np.reciprocal(ADSINR)
    return ADSINR

def MVDR_2D_Beamformer_Weights(rx,steering_vectors,DoA):
    R = np.corrcoef(rx)
    #R = forward_backward_avg(R)
    #R = spatial_smoothing(rx.T,4,direction = "forward-backward")
    R_inv  = np.linalg.inv(R) # invert the cross correlation matrix
    S_theta = steering_vectors[:,:,DoA[0],DoA[1]]
    weights = np.dot(R_inv,S_theta)/np.dot(np.matrix(S_theta).H,np.dot(R_inv,S_theta))[0,0]
    return weights

def MVDR_2D_Beamformer(rx, weights):
    weighted_rx = np.dot(rx.T,weights)
    return weighted_rx

def MVDR_Block(rx, steering_vectors,incident_thetas,incident_phis,start,end,block_size):
    amt_of_blocks = int((end-start)/block_size)
    weighted_rec_signal = np.empty(shape = (end-start,1))
    DoA_Array = np.empty(shape = (amt_of_blocks,2))
    for k in range(amt_of_blocks):
        block_start = k*block_size
        block_end = (k+1)*block_size
        DoA_spectrum = DoA_MVDR(rx[:,block_start:block_end],steering_vectors,incident_thetas, incident_phis)
        DoA = np.unravel_index(np.argmin(np.abs(DoA_spectrum)), DoA_spectrum.shape)
        DoA_Array[k,:] = DoA
        weights = MVDR_2D_Beamformer_Weights(rx[:,block_start:block_end],steering_vectors,DoA)
        weighted_rec_signal[block_start:block_end,:] = MVDR_2D_Beamformer(rx[:,block_start:block_end], weights)
    return weighted_rec_signal, DoA_Array

def beamforming (file1, file2, file3, file4):
	## Create Phased Array
	d = 0.5 # Inter element spacing [lambda]
	M_x = 2  # number of antenna elements in the x axis
	M_y = 2 # number of antenna elements in the y axis
	array_alignment_x = np.arange(0, M_x, 1)* d; # Creates array in x direction of half-wavelength magnitudes
	array_alignment_y = np.arange(0, M_y, 1)* d; # Creates array in xy direction of half-wavelength magnitudes

	# Calulate Steering Vector
	angles = 181
	incident_thetas= np.arange(0,91,1)
	incident_phis = np.arange(0,361,1)
	steering_vectors = gen_steering_vectors(array_alignment_x, array_alignment_y, incident_thetas, incident_phis)

	# Load test data into each antenna
	antenna_1 = np.fromfile(file1, dtype="float32")  # Loads data as float32 format
	antenna_1 = antenna_1.astype(np.float32).view(np.complex64) # Converts to float64 complex
	antenna_2 = np.fromfile(file2, dtype="float32")  # Loads data as float32 format
	antenna_2 = antenna_2.astype(np.float32).view(np.complex64) # Converts to float64 complex
	antenna_3 = np.fromfile(file3, dtype="float32")  # Loads data as float32 format
	antenna_3 = antenna_3.astype(np.float32).view(np.complex64) # Converts to float64 complex
	antenna_4 = np.fromfile(file4, dtype="float32")  # Loads data as float32 format
	antenna_4 = antenna_4.astype(np.float32).view(np.complex64) # Converts to float64 complex

	start = 1000000
	end = 1400001
	end_of_file = 1413632
	block_size = end-start
	rec_signal = np.vstack((antenna_1[start:end].T,antenna_2[start:end].T,antenna_3[start:end].T,antenna_4[start:end].T))

	[weighted_rec_signal,DoA] = MVDR_Block(rec_signal,steering_vectors,incident_thetas,incident_phis,start,end,block_size)

	# Save to binary file
	complex64_weighted_rec_signal = weighted_rec_signal.astype(np.complex64)
	re = np.real(complex64_weighted_rec_signal)
	im = np.imag(complex64_weighted_rec_signal)
	raw_data = np.empty((re.size + im.size,), dtype=re.dtype)
	raw_data[0::2] = re.T
	raw_data[1::2] = im.T
	raw_data.astype("float32").tofile("data_out")


def snr_calc(file1, beamfile):
	single = read_binary_iq(file1)
	beamformed = read_binary_iq(beamfile)
	psingle = np.abs(single)
	pbeamformed = np.abs(beamformed)
	snr_len = len(psingle)/10000
	snr_arr = np.zeros((snr_len, 2), dtype=float)

	for i in range(snr_len):
		single_arr = psingle[i:i+10000]
		beam_arr = pbeamformed[i:i+10000]
		snr_arr[i,0] = signaltonoise(single_arr, axis =0, ddof = 0)
		snr_arr[i,1] = signaltonoise(beam_arr, axis=0, ddof=0)
 

    #plt.figure()
	plt.plot(20*np.log10(snr_arr[:,0]))
	plt.plot(20*np.log10(snr_arr[:,1]))
	plt.title("SNR comparison")
	plt.xlabel("Samples*10k")
	plt.ylabel("dB")
	plt.legend(["Single stream", "Beamformed"])
	plt.grid()
	plt.show()


def test_beamforming_algo():
	print ("")
	sdr_1 = "sdr_1"
	sdr_2 = "sdr_2"
	sdr_3 = "sdr_3"
	sdr_4 = "sdr_4"
	data_out = "data_out"

	#set up flowgraph commands
	flowgraphname = "python /home/marissa/Documents/Rutgers/capstone/iq_stream.py -a {file1} -b {file2} -c {file3} -d {file4}". format(
		file1 = sdr_1,
		file2 = sdr_2,
		file3 = sdr_3,
		file4 = sdr_4,
	)

	runcmd = "{cmd}".format(
		cmd = flowgraphname
	)

	print runcmd
	testapp = pexpect.spawn(runcmd)

	#run it
	try_flowgraph_expect(testapp, 30)
	print ("Flowgraph started")

	#wait for a bit
	time.sleep(5)

	#Kill flowgraph
	print ("Flowgraph closing")
	#testapp.sendline("\r\n")
	time.sleep(1)
	testapp.sendcontrol("c")
	try_eof_expect(testapp, timeout=10)

	#use beamforming algorithm
	beamforming(sdr_1, sdr_2, sdr_3, sdr_4)
	print ("beamforming done")
	#data_out = weighted
	snr_calc(sdr_1, data_out)

if __name__ == '__main__':    
    
    test_beamforming_algo()
    print('done')
    exit(0)