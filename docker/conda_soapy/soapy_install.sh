#!/bin/bash
# Add SoapySDR PPA to your system
sudo add-apt-repository -y ppa:myriadrf/drivers
# Update list of packages
sudo apt-get update
# Install basic dependencies
sudo apt-get install -y python3-pip python3-numpy python3-scipy soapysdr python3-soapysdr
# Install SoapySDR RTL-SDR drivers 
sudo apt-get install -y soapysdr-module-rtlsdr 
