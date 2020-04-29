#!/bin/bash
# conda installer jetson docker
set -euxo pipefail
fname="c4aarch64_installer-1.0.0-Linux-aarch64.sh"
wget https://github.com/jjhelmus/conda4aarch64/releases/download/1.0.0/$fname
# chmod +x c4aarch64_installer-1.0.0-Linux-aarch64.sh
bash -x c4aarch64_installer-1.0.0-Linux-aarch64.sh -bfp /opt/conda
/opt/conda/bin/conda clean -ptiy
rm -rf $fname
