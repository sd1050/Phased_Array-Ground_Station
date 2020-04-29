FROM nvcr.io/nvidia/l4t-base:r32.3.1
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && apt-get install -y tzdata
RUN apt-get update && apt-get install -y --fix-missing make g++
RUN apt-get update && apt-get install -y --fix-missing python-pip 
RUN apt-get update && apt-get install -y --fix-missing gnuradio
RUN apt-get update && apt-get install -y --fix-missing swig doxygen
RUN PATH=/usr/local/cuda-10.0/bin:${PATH} pip install -U pycuda
CMD [ "bash" ]