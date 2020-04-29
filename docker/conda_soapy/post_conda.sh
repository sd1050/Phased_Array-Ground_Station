#!/bin/bash
# Activate environment to link
source /opt/conda/etc/profile.d/conda.sh
conda activate cusignal
# Point to conda path
CONDA_PACKAGE_PATH=$(python -c 'import site; print(site.getsitepackages()[0])')
# Create symbolic links for SoapySDR to the Conda environment and see it
SOAPY_INSTALL_DIR="/usr/lib/python3/dist-packages"
SOAPY_FILE_NAMES="_SoapySDR.cpython-36m-aarch64-linux-gnu.so SoapySDR.py"
for file_name in ${SOAPY_FILE_NAMES}; do
    src_file="${SOAPY_INSTALL_DIR}/${file_name}"
    if [[ -f ${src_file} ]]; then
        ln -s ${src_file} ${CONDA_PACKAGE_PATH}/${file_name}
        if [[ $? -eq 0 ]] ; then
            echo "Successfully created symbolic link:"
            echo "  ${src_file} -> "
            echo "  ${CONDA_PACKAGE_PATH}/${file_name}"
        fi
    else
        echo "Source file does not exist: ${src_file}"
        echo "Make sure SoapySDR drivers are properly installed."
    fi
done
export LD_LIBRARY_PATH=${SOAPY_INSTALL_DIR}
# simplesoapy
cd ~/
git clone https://github.com/xmikos/simplesoapy.git
cd simplesoapy
python3 setup.py build
python3 setup.py install
pip3 install -U cython pyfftw