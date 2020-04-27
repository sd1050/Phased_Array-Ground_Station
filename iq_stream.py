#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Iq Stream
# GNU Radio version: 3.7.13.5
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt


class iq_stream(gr.top_block):

    def __init__(self, file1="sync-stream1-2", file2="sync-stream2-2", file3="sync-stream2-2", file4="sync-stream2-2"):
        gr.top_block.__init__(self, "Iq Stream")

        ##################################################
        # Parameters
        ##################################################
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3
        self.file4 = file4

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_file_source_0_2 = blocks.file_source(gr.sizeof_gr_complex*1, 'SDR4', False)
        self.blocks_file_source_0_2.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_gr_complex*1, 'SDR2', False)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'SDR3', False)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'SDR1', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_2 = blocks.file_sink(gr.sizeof_gr_complex*1, file4, False)
        self.blocks_file_sink_0_2.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, file2, False)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file3, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file1, False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.blocks_file_source_0_2, 0), (self.blocks_file_sink_0_2, 0))

    def get_file1(self):
        return self.file1

    def set_file1(self, file1):
        self.file1 = file1
        self.blocks_file_sink_0.open(self.file1)

    def get_file2(self):
        return self.file2

    def set_file2(self, file2):
        self.file2 = file2
        self.blocks_file_sink_0_1.open(self.file2)

    def get_file3(self):
        return self.file3

    def set_file3(self, file3):
        self.file3 = file3
        self.blocks_file_sink_0_0.open(self.file3)

    def get_file4(self):
        return self.file4

    def set_file4(self, file4):
        self.file4 = file4
        self.blocks_file_sink_0_2.open(self.file4)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-a", "--file1", dest="file1", type="string", default="sync-stream1-2",
        help="Set sync-stream1-2 [default=%default]")
    parser.add_option(
        "-b", "--file2", dest="file2", type="string", default="sync-stream2-2",
        help="Set sync-stream2-2 [default=%default]")
    parser.add_option(
        "-c", "--file3", dest="file3", type="string", default="sync-stream2-2",
        help="Set sync-stream2-2 [default=%default]")
    parser.add_option(
        "-d", "--file4", dest="file4", type="string", default="sync-stream2-2",
        help="Set sync-stream2-2 [default=%default]")
    return parser


def main(top_block_cls=iq_stream, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(file1=options.file1, file2=options.file2, file3=options.file3, file4=options.file4)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
