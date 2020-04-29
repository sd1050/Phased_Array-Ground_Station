# FROM nvcr.io/nvidia/l4t-base:r32.3.1
FROM sd1050/ground_station:soapy_conda_cusignal-1.1
WORKDIR /Ground_Station/build_scripts
# COPY soapy_install.sh /Ground_Station/build_scripts
# COPY conda_install.sh /Ground_Station/build_scripts
COPY conda_post_install.sh /Ground_Station/build_scripts
# COPY post_conda.sh /Ground_Station/build_scripts
COPY cusignal.yml /Ground_Station/build_scripts
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive 
# RUN apt-get update && apt-get install -y tzdata
# RUN apt-get update && apt-get install -y software-properties-common git
# RUN apt-get update && apt-get install -y --fix-missing make g++ 
# RUN chmod +x soapy_install.sh; ./soapy_install.sh
# RUN chmod +x conda_install.sh; ./conda_install.sh
WORKDIR /Ground_Station
RUN chmod +x build_scripts/conda_post_install.sh; ./build_scripts/conda_post_install.sh
# RUN chmod +x post_conda.sh; ./post_conda.sh
CMD [ "bash" ]