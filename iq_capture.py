#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Inmarsat-C BPSK demodulator(s)
# Author: GNU General Public License 3, microp11 2018
# Description: The default settings are for an AirSpy device on Inmarsat 4F3 54W
# GNU Radio version: 3.7.13.5
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import multi_rtl


class iq_capture(gr.top_block):

    def __init__(self, file1="sync-stream1-2", file2="sync-stream2-2"):
        gr.top_block.__init__(self, "Inmarsat-C BPSK demodulator(s)")

        ##################################################
        # Parameters
        ##################################################
        self.file1 = file1
        self.file2 = file2

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = 1200
        self.samp_rate_demod = samp_rate_demod = 48000

        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0 = firdes.root_raised_cosine(15, samp_rate_demod, symbol_rate, 0.35, 11*(samp_rate_demod/symbol_rate))

        self.samp_rate = samp_rate = 2.5e6
        self.channel_width = channel_width = 4000
        self.center_freq = center_freq = 1540e6

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate_demod/1000),
                decimation=100,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate_demod/1000),
                decimation=100,
                taps=None,
                fractional_bw=None,
        )
        self.multi_rtl_source_0 = multi_rtl.multi_rtl_source(sample_rate=samp_rate, num_channels=2, ppm=0, sync_center_freq=1535e6, rtlsdr_id_strings= [
          "0",
          "1",
          "2",
          "3",
          "4",
          "5",
          "6",
          "7",
          "8",
          "9",
          "10",
          "11",
          "12",
          "13",
          "14",
          "15",
          "16",
          "17",
          "18",
          "19",
          "20",
          "21",
          "22",
          "23",
          "24",
          "25",
          "26",
          "27",
          "28",
          "29",
          "30",
          "31",
          ])
        self.multi_rtl_source_0.set_sync_gain(10, 0)
        self.multi_rtl_source_0.set_gain(20, 0)
        self.multi_rtl_source_0.set_center_freq(center_freq, 0)
        self.multi_rtl_source_0.set_gain_mode(False, 0)
        self.multi_rtl_source_0.set_sync_gain(10, 1)
        self.multi_rtl_source_0.set_gain(20, 1)
        self.multi_rtl_source_0.set_center_freq(center_freq, 1)
        self.multi_rtl_source_0.set_gain_mode(False, 1)

        self.low_pass_filter_0_1 = filter.fir_filter_ccf(25, firdes.low_pass(
        	10, samp_rate, 50000, 1000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(25, firdes.low_pass(
        	10, samp_rate, 50000, 1000, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file2, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file1, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.multi_rtl_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.multi_rtl_source_0, 1), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_file_sink_0_0, 0))

    def get_file1(self):
        return self.file1

    def set_file1(self, file1):
        self.file1 = file1
        self.blocks_file_sink_0.open(self.file1)

    def get_file2(self):
        return self.file2

    def set_file2(self, file2):
        self.file2 = file2
        self.blocks_file_sink_0_0.open(self.file2)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_samp_rate_demod(self):
        return self.samp_rate_demod

    def set_samp_rate_demod(self, samp_rate_demod):
        self.samp_rate_demod = samp_rate_demod

    def get_variable_rrc_filter_taps_0(self):
        return self.variable_rrc_filter_taps_0

    def set_variable_rrc_filter_taps_0(self, variable_rrc_filter_taps_0):
        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(10, self.samp_rate, 50000, 1000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(10, self.samp_rate, 50000, 1000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.multi_rtl_source_0.set_center_freq(self.center_freq, 0)
        self.multi_rtl_source_0.set_center_freq(self.center_freq, 1)
        self.analog_sig_source_x_0_1.set_frequency(self.center_freq)
        self.analog_sig_source_x_0.set_frequency(self.center_freq)


def argument_parser():
    description = 'The default settings are for an AirSpy device on Inmarsat 4F3 54W'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "-f", "--file1", dest="file1", type="string", default="sync-stream1-2",
        help="Set sync-stream1-2 [default=%default]")
    parser.add_option(
        "-e", "--file2", dest="file2", type="string", default="sync-stream2-2",
        help="Set sync-stream2-2 [default=%default]")
    return parser


def main(top_block_cls=iq_capture, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(file1=options.file1, file2=options.file2)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
