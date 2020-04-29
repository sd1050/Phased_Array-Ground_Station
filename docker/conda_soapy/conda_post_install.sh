#!/bin/bash
# post-conda installs

# source /opt/conda/etc/profile.d/conda.sh
# conda activate base
# conda config --add channels c4aarch64
# conda config --add channels conda-forge
# conda config --set auto_activate_base false 
# conda create --name cusignal python=3.6
# conda activate cusignal
# conda install numpy scipy pip

source /opt/conda/etc/profile.d/conda.sh
conda activate cusignal
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin 
mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
apt-key add /var/cuda-repo-10-0-local-10.0.107-435.17.01/7fa2af80.pub
apt-get update
apt-get -y install cuda
# conda install -c anaconda numpy spicy cudatoolkit pip 
# | cat /usr/local/cuda-10.0/version.txt
# conda remove -y --name cusignal --all
# pip install -U setuptools pip
# nvcc --version
# conda install -c numba numba
# export NVCC='ccache nvcc'
# export CUDA_PATH=/usr/local/cuda-10.0
# export LD_LIBRARY_PATH=$CUDA_PATH/lib64:$LD_LIBRARY_PATH
# CUDA_PATH=/usr/local/cuda-10.0 
# apt-get install g++
# export CPATH=/usr/local/include
# export LIBRARY_PATH=/usr/local/lib
# export LDFLAGS="-L/usr/local/lib"
# export PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}
# export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# sudo apt-get update
# pip install cython
# pip install wheels
# export CUDA_PATH=/Developer/NVIDIA/CUDA-10.0
pip install cupy-cuda100
# export CUSIGNAL_HOME=$(pwd)/cusignal
# git clone https://github.com/rapidsai/cusignal.git $CUSIGNAL_HOME
# cd $CUSIGNAL_HOME
# conda env create -f conda/environments/cusignal_jetson_base.yml

# conda activate cusignal

# cd $CUSIGNAL_HOME/python
# python setup.py install

# pytest -v
