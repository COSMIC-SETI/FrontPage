Software source and other files cloned/saved to /home/cosmic/src, primarily, /home/cosmic/dev secondarily.

# Computer Setup

## [Adjust BIOS for HPC](https://hpcadvisorycouncil.atlassian.net/wiki/spaces/HPCWORKS/pages/1280442391/AMD+2nd+Gen+EPYC+CPU+Tuning+Guide+for+InfiniBand+HPC?focusedCommentId=2152333319)

- `APBDIS = 1 [NB Configuration]`
- `Fixed SOC Pstate = P0 [NB Configuration]`
- `IOMMU = disabled [NB Configuration]`
- `DF Cstates = disabled [NB Configuration]`
- `SMT = disabled [CPU Configuration]`
- `Local APIC mode = x2APIC [CPU Configuration]`
- `NUMA nodes per socket = NPS1 [ACPI Settings]`
- `L3 cache as NUMA = disabled [ACPI Settings (ACPI SRAT L3 Cache As NUMA Domain)] {{{ it’s recommended to be enabled, but then causes too many NUMA nodes - Ross }}}`
- `PCIe Relaxed Ordering = enabled [PCIe/PCI/PnP Configuration]`


## [Install Mellanox Drivers](https://docs.mellanox.com/display/MLNXOFEDv531001/Installing+Mellanox+OFED)
[Download](https://www.mellanox.com/products/infiniband-drivers/linux/mlnx_ofed) tar.gz and extract
```
# ./mlnxofedinstall --force --dkms --disable-affinity --basic
# /etc/init.d/openibd restart
```

Verification is achieved with `ibv_devinfo` listing the expected number of devices.

## Install CUDA and Nvidia driver
```
$ ​​wget https://developer.download.nvidia.com/compute/cuda/11.4.1/local_installers/cuda_11.4.1_470.57.02_linux.run
# /bin/sh cuda_11.4.1_470.57.02_linux.run --toolkit --samples --installpath=/usr/local/cuda-11.4.1 --no-opengl-libs
# /bin/bash NVIDIA-Linux-x86_64-*.run --dkms --no-drm --no-opengl-files
```
Add to /etc/bash.bashrc
```
# CUDA stuff

export CUDA_VER="11.1.1"
export CUDA_ROOT="/usr/local/cuda-${CUDA_VER}"
export CUDA_NVCC_FLAGS="-O3 -gencode arch=compute_30,code=sm_30 -gencode arch=compute_52,code=sm_52 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_75,code=sm_75 -lineinfo -maxrregcount 64"

export PATH=${PATH}:${CUDA_ROOT}/bin
[[ -z "${LD_LIBRARY_PATH}" ]] &&
    export LD_LIBRARY_PATH="${CUDA_ROOT}/lib64" ||
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:"${CUDA_ROOT}/lib64"
```

Verify after reboot:
```
$ nvidia-smi

lspci -nnk | grep -iA2 vga output below with the successful registration of nvidia emboldened.

3b:00.0 VGA compatible controller [0300]: NVIDIA Corporation TU102 [GeForce RTX 2080 Ti] [10de:1e04] (rev a1)
        Subsystem: eVga.com. Corp. TU102 [GeForce RTX 2080 Ti] [3842:2281]
        Kernel driver in use: nvidia
        Kernel modules: nvidiafb, nouveau, nvidia
```

## Format and RAID0 drives
```
# mdadm -Cv -l0 -n4 /dev/md126 /dev/nvme{0,1,2,3}n1
# mdadm -Cv -l0 -n4 /dev/md127 /dev/nvme{4,5,6,7}n1
# mkfs.xfs /dev/md126
# mkfs.xfs /dev/md127
# mkdir /mnt/buf0
# mkdir /mnt/buf1
# mount /dev/md126 /mnt/buf0
# mount /dev/md127 /mnt/buf1
```

# Software Setup

## General package install:
`# apt install automake gfortran numactl ruby-dev linux-tools-$(uname -r) liberfa-dev libhdf5-dev libspdlog-dev package-conf gcc-10 g++-10`

### Clone [hashpipe](https://github.com/MydonSolutions/hashpipe/tree/seti_ata_ibv)
```
./configure --prefix=/home/cosmic/dev/hashpipe/install
make
```

### Clone [pyslalib](https://github.com/scottransom/pyslalib)
```
make
```

### Clone [uvh5c99](https://github.com/MydonSolutions/uvh5c99)
```
git submodule update –recursive
cd external_src/radiointerferometry && meson builddir && cd builddir && ninja && cd ../../../
meson build && cd build && ninja test
```

### Clone [blade](https://github.com/luigifcruz/blade)`
```
CC=gcc-10 CXX=g++-10 meson build && cd build && ninja test
```

### Clone [xGPU](https://github.com/GPU-correlators/xGPU)
```
make NTIME=32768 NTIME_PIPE=128 NPOL=2 NFREQUENCY=512 NSTATION=16 CUDA_ARCH=sm_86 DP4A=yes
```

### Clone [hpguppi](https://github.com/MydonSolutions/hpguppi_daq/tree/seti-ata-8bit)
```
CXX=g++-10 ./configure --with-libsla=/home/cosmic/dev/pyslalib --with-hashpipe=/home/cosmic/dev/hashpipe/src/.libs --with-libblade=/home/cosmic/src/blade/build --with-cuda-include=/usr/local/cuda-11.4.1/include --with-libxgpu=/home/cosmic/src/xGPU/src/ --with-xgpu-include=/home/cosmic/src/xGPU/src --with-libuvh5=/home/cosmic/src/uvh5c99/build
make
```

### Clone [rb-hashpipe](https://github.com/david-macmahon/rb-hashpipe)
```
$ rake package 
# apt install libncurses5-dev
# pkg gem install --local ./hashpipe-0.6.3.gem -- --with-hashpipe-include=/home/cosmic/dev/hashpipe/src --with-hashpipestatus-lib=/home/cosmic/dev/hashpipe/src/.libs
```

## Clone [rawspec](https://github.com/UCBerkeleySETI/rawspec)
```
make
```

Add to /etc/bash.bashrc
```
# Rawspec stuff
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:"/home/cosmic/src/rawspec"
export PATH=${PATH}:/home/cosmic/src/rawspec
```

## [Julia](https://julialang.org/downloads/) 
```
$ cd /home/cosmic/dev
$ wget https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.6-linux-x86_64.tar.gz
$ tar -xvf ./julia-1.6.6-linux-x86_64.tar.gz
```

Add to /etc/bash.bashrc
```
# Julia stuff
export PATH=${PATH}:/home/cosmic/dev/julia-1.6.6/bin
```
