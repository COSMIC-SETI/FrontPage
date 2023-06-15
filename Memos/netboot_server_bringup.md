
# Netboot Server Configuration
Author: Jack Hickish
Date: 26th May 2023

## Introduction

Like many SETI CPU/GPU processing clusters, COSMIC utilizes a netboot server to provide a common operating system image to all nodes in the cluster.
In this document the steps necessary to add new nodes to the COSMIC cluster are described, as well as the node-specific configuration steps required.

## Netboot Server Configuration

In the COSMIC system, the server `cosmic-head` provides netboot functionality to all nodes in the cluster.
This functionality has multiple components:

  - A DHCP server, to provide IP addresses to nodes on the COSMIC network.
  - A TFTP server, to provide the initial boot image to nodes.
  - An NFS server, to provide a common read-only Operating System image and shared `/home` directory to all nodes.

DHCP and TFTP services are provided by the `dnsmasq` package, while NFS services are provided by the `nfs-kernel-server` package.

The [cosmic-netboot git repository](https://github.com:COSMIC-SETI/cosmic-netboot.git) provides configuration files which COSMIC-specific configuration files such as MAC and IP address mappings. This repository also tracks [netboot\_resources](https://github.com/david-macmahon/netboot_resources.git) as submodule, which contains general purpose netboot configuration instructions and tools. The rest of this document assumes that a netboot infrastructure has been created using the tools in this repository.

### Netboot mounts

The COSMIC netboot `fstab` file (which is on the head node at `/srv/jammy/netboot/fstab`) contains the following entries.

```fstab
# NFS mounts
192.168.32.1:/srv/jammy/rootfs.amd64  /      nfs  ro,hard,nointr,nfsvers=3  0  0
192.168.32.1:/home                    /home  nfs  rw,hard,nointr,nfsvers=3  0  0

# tmpfs filesystems
none  /tmp           tmpfs  mode=1777,rw,nosuid,nodev,noexec  0  0
none  /dev/shm       tmpfs  mode=1777,rw,nosuid,nodev,noexec  0  0
none  /var/lib/sudo  tmpfs  mode=0700,rw,nosuid,nodev,noexec  0  0

# RAIDs (only present on GPU nodes)
/dev/hptblock0n0p /mnt/buf0 xfs defaults,nofail 0 0
/dev/hptblock0n1p /mnt/buf1 xfs defaults,nofail 0 0

# Local scratch (sometimes present on nodes)
/dev/disk/by-label/scratch /mnt/scratch ext4 defaults,nofail 0 0

# High capacity volumes (only present on storage nodes)
/dev/disk/by-label/data0 /srv/data0 xfs defaults,nofail 0 0
/dev/disk/by-label/data1 /srv/data1 xfs defaults,nofail 0 0
/dev/disk/by-label/data2 /srv/data2 xfs defaults,nofail 0 0
```

Netboot nodes will attempt to mount these volumes whether or not they exist, and quiet failure is relied upon when they don't.
Managing volumes in this way makes it easy to use a shared `fstab` with multiple, differently configured, netboot nodes.
In the future, this may or may not turn out to be a viable strategy.

## Adding a New Netboot Node

To add a new node to the COSMIC cluster:

### Add a new canonical hostname and MAC addresses

A new hostname should be added to the `canonical_names` list in the file `cosmic-netboot/group_vars/all/canonical_names.yml`. These hostnames are designed to be unique throughout the wider COSMIC group's infrastructure, and are generally chosen to reflect the node's physical hardware rather than its function in the cluster.

The MAC addresses for the new server's IPMI and `eth0` interfaces should be added for the new hostname.
For example:

```yaml
canonical_names:
    # Pre-existing hosts
    acmea17: # Acme => purchased from ACME Micro; a=> AMD CPU
        ipmi_mac: 00:25:90:00:00:00 # IPMI MAC address
        eth0_mac: 00:25:90:00:00:01 # eth0 MAC address
```

### Configure the new node's IP address

Define the IP address for the IPMI and `eth0` interfaces of the new node by configuring them in `cosmic-netboot/hosts.yml`.
For example:

```yaml
  children:
    head_nodes:
      hosts:
        cosmic-head:
          canonical_name: head0
          ansible_connection: local

    # Used to run ansible playbooks in chroot-ed netboot root file system
    netboot_chroot:
      hosts:
        netboot_root:
          ansible_connection: chroot
          ansible_host: "{{ netboot_root }}"

    # Hosts in the `netboot_nodes` group will have /etc/ethers and /etc/hosts
    # entries managed for them based on the mappings in `canonical_names.yml`
    # and the host variables `canonical_name`, `eth0_ip`, and `ipmi_ip` host
    # variables defined in this file for hosts in the netboot group.
    netboot_nodes:
      children:
        compute_nodes:
          hosts:
            cosmic-gpu-12:
              canonical_name: acmea17
              eth0_ip: 192.168.32.110
              ipmi_ip: 192.168.33.110
```

This configuration entry will assign the new node's `eth0` IP as `192.168.32.110` and its IPMI IP as `192.168.33.110`.
The node will also be assigned the logical hostname `cosmic-gpu-12`.
The mapping of logical to canonical hostnames using this configuration file means that hardware swaps can be implemented by simply changing the `canonical_name` variable for a given node.

### Reconfigure `dnsmasq`

In order for the new IP settings to take effect, the head node's `/etc/ethers` file (which stores MAC addresses) and `/etc/hosts` file (which stores hostname to IP mappings) must be updated.
This is accomplished by running the `ether-hosts` ansible playbook:

```bash
ansible-playbook -K cosmic-netboot/netboot_resources/playbooks/ether-hosts.yml
```

This playbook will automatically modify `/etc/ethers` and `/etc/hosts` and restart `dnsmasq` so that the new settings take effect.
Once this is complete, the new node should be able to boot from the netboot server with a correct IP address and hostname.

### Add Persistent File Systems

The netboot server provides a common read-only root file system to all nodes in the cluster, which is not sufficient for some applications to function correctly.
Therefore, a separate persistent file system, which is unique to each node, is also hosted by the netboot server, and mounted at `/mnt/persistent` on each node.

The persistent file systems live on the head node at `/srv/jammy/persistent`, and are named after a node's canonical hostname.
For example, if a new node has canonical hostname `acmea17`, then its persistent file system will be located at `/srv/jammy/persistent/acmea17`.
Symbolic links are created so that the logical hostnames of nodes can also be used, e.g. `/srv/jammy/persistent/cosmic-gpu-12`.

### Highpoint NVMe RAID Configuration

> *NB: This section is only relevant for nodes with Highpoint NVMe RAID controllers. Typically this is only the GPU processing nodes.*

The COSMIC GPU nodes are equipped with [Highpoint SSD7540](https://www.highpoint-tech.com/nvme1/ssd7540) NVMe RAID controllers (See the COSMIC [Hardware](../Infrastructure/Hardware.md) document).

These need to be configured prior to using the system's NVME, which currently is not automated.

#### Highpoint Driver Installation

> *NB: This process only needs to be carried out when the first Highpoint NVMe-enabled node is added to the cluster.*


1. Install the Highpoint drivers and configuration tool.

    1. Download the Highpoint Linux Opensource Driver, and Linux RAID Management Software from [Highpoint SSD7540](https://www.highpoint-tech.com/nvme1/ssd7540).

    2. [from the Highpoint-enabled netboot node] Install these packages.

        ```
        # Mount the rootfs writable to enable installation
        mount -o remount,rw /
        # Executables are extracted to /tmp so this hsould be executable
        mount -o remount,exec /tmp
        tar -xzf HighPoint_NVMe_G5_Linux*.tar.gz
        ./hptnvme_g5_linux*.bin
        tar -xzf RAID_Manage_Linux*.tgz
        ./RAID_Manage_Linux*.sh
        # Remount /tmp in original state
        mount -o remount,noexec /tmp
        ```

    3. Configure RAID Management
    
        ```
        # Move newly created Highpoint files to persistent storage
        mv /etc/hptuser.dat /persistent/etc/hptuser.dat
        mv /etc/hptrec.bin /persistent/etc/hptrec.bin
        mv /usr/share/hpt /persistent/usr/share/hpt
        # Symlink so that software can still find them
        ln -s /persistent/etc/hptuser.dat /etc/hptuser.dat
        ln -s /persistent/etc/hptrec.bin /etc/hptrec.bin
        ln -s /persistent/usr/share/hpt /usr/share/hpt

        # Start RAID control server
        systemctl statrt hptsvr.service
        # Connect to controller
        hptraidconf
        # In CLI, set password to 'cosmic'
        set PS
        exit
        # Remount root filesystem in original state
        mount -o remount,ro /
        ```

#### Configure RAID drives

A manual for the Highpoint RAID configuration CLI is available at (https://www.highpoint-tech.com/gen4-nvme-m2).
The following script will automatically configure the RAID cards for the COSMIC GPU nodes, assuming that each node contains two RAID cards and each is connected to 8 NVMe drives.

```bash
for i in {1..8}; do hptraidconf init 1/E1/$i -u RAID -p cosmic; done
for i in {1..8}; do hptraidconf init 1/E2/$i -u RAID -p cosmic; done
sleep 1

# Why is this needed here?
/etc/init.d/hptdaemon stop
/etc/init.d/hptdaemon start
hptsvr 
sleep 3

hptraidconf create RAID0 disks=1/E1/1,1/E1/2,1/E1/3,1/E1/4,1/E1/5,1/E1/6,1/E1/7,1/E1/8 init=quickinit -u RAID -p cosmic
hptraidconf create RAID0 disks=1/E2/1,1/E2/2,1/E2/3,1/E2/4,1/E2/5,1/E2/6,1/E2/7,1/E2/8 init=quickinit -u RAID -p cosmic
# Format xfs
# Device names here will depend what was initially set up before these configs.
# The fstab assumes the devices will be called hptblock0n[0,1]p after reboot. But they might have different names right now
for dev in `ls /dev/hptblock0n*`; do mkfs.xfs $dev; done
```

On reboot, these devices should be correctly configured and mounted.

### Scratch Space

If a new server has a scratch disk, provided it is labelled "scratch" it will be mounted at `/mnt/scratch`.

Most of the COSMIC GPU nodes have a scratch disk at `/dev/sda`, which can be configured with:

```
fdisk /dev/sda
g # Create GPT partition table
n # Create a new partition
1 # First partition
[enter] # Starting point to first sector (default)
[enter] # Ending point to last sector (default)
w # write changes

<exit>
# Format the partition
mkfs.ext3 -L scratch /dev/sda1
```

### Configure Bulk Storage

> *NB: This section is likely only relevant for storage nodes*

Each COSMIC storage node has 36 spinning disks, which are configured as 3 individual 11-disk RAID6 volumes, plus 3 global hot spares.

The following configuration steps (run on the relevant storage node) will achieve this.

```bash
# how to get all info from controller
# run as sudo / root to actually get useful command responses

storcli /c0 show # assuming "c0" is the controller id, which is usually the case but not guaranteed!

# on cosmic-storage-{1..2} I see on /c0 there are two "enclosures" (24 drives on front, 12 on back)
# and the two enclosure are:
#
# e250 - 12 drives in back (slots {0..11})
# e251 - 24 drives in front (slots {0..23})
#
# these can be wildly different numbers on each host - be careful!

# first clean out all current "disk group" and "foreign" configurations - this is destructive - be careful!

storcli /c0/vall delete #-force # delete all current disk groups
storcli /c0/fall delete # remove all foreign configurations

# are there any spare drives? delete those configs as well:

storcli /cx/ex/sx delete hotsparedrive # enter in the correct controller/enclosure/slot info of course

# build raids

storcli /c0 add vd type=raid6 drives='250:0,250:1,250:2,250:3,250:4,250:5,250:6,250:7,250:8,250:9,250:10'
storcli /c0 add vd type=raid6 drives='251:0,251:1,251:2,251:3,251:4,251:5,251:6,251:7,251:8,251:9,251:10'
storcli /c0 add vd type=raid6 drives='251:12,251:13,251:14,251:15,251:16,251:17,251:18,251:19,251:20,251:21,251:22'

# At this point if you run "fdisk" you should see three equally sized drives with names like /dev/sd{a,b,c} 
# Note that even after rebooting the order how RAID disk groups get assigned to dev names may change!!!!
# In other words: never trust this relationship ever! (mount by disk label, not dev name, for example)

# add hot spares

storcli /c0/e250/s11 add hotsparedrive
storcli /c0/e251/s11 add hotsparedrive
storcli /c0/e251/s23 add hotsparedrive
```

These RAID volumes then need partitioning:

```bash
# Create partitions on each RAID volume using fdisk
fdisk /dev/sda # or whatever the device name is
g # Create GPT partition table
n # Create a new partition
1 # First partition
[enter] # Starting point to first sector (default)
[enter] # Ending point to last sector (default)
w # write changes
exit

fdisk /dev/sdb # or whatever the device name is
g # Create GPT partition table
n # Create a new partition
1 # First partition
[enter] # Starting point to first sector (default)
[enter] # Ending point to last sector (default)
w # write changes
exit

fdisk /dev/sdc # or whatever the device name is
g # Create GPT partition table
n # Create a new partition
1 # First partition
[enter] # Starting point to first sector (default)
[enter] # Ending point to last sector (default)
w # write changes
exit
```

And finally, formatting:

```bash
mkfs.xfs -L data0 /dev/sda1
mkfs.xfs -L data1 /dev/sdb1
mkfs.xfs -L data2 /dev/sdc1
```

Providing these volumes are labelled `data0`, `data1` and `data2`, they will be automatically mounted at boot.

## NFS Mounts

While `fstab` is used to manage the mounting of local volumes, [`autofs`](https://help.ubuntu.com/community/Autofs) is used to manage the mounting of NFS file systems.

If a server is added to the system which hosts a filesystem that netboot nodes should mount, the following steps should be taken:

1. On the netboot filesystem, add a file `auto.<new-server-name>` which contains information about the NFS volumes on this server which other machines should mount. For example, `/etc/auto.cosmic-storage-1` contains:

    ```
    data0 -fstype=nfs,nfsvers=3,rw,hard,nointr cosmic-storage-1-100g-0:/srv/data0
    data1 -fstype=nfs,nfsvers=3,rw,hard,nointr cosmic-storage-1-100g-0:/srv/data1
    data2 -fstype=nfs,nfsvers=3,rw,hard,nointr cosmic-storage-1-100g-0:/srv/data2
    ```
2. Add a line in `/etc/auto.master` which points to this file.
For example:

    ```
    /cosmic-storage-1 /etc/auto.cosmic-storage-1 --timeout=180
    ```

## 100G IP Addressing

A simple script, which runs at boot via `root`'s `crontab`, is used to configure 100G interfaces on the cluster node, based on hostnames.

This script is:

```bash
#! /bin/bash

BASEIP0="192.168.64."
BASEIP1="192.168.65."
declare -A IP_OFFSET
IP_OFFSET=(["storage"]=10 ["gpu"]=100)

declare -A IF0SD
IF0SD=(["storage"]="enp175s0f1np1" ["gpu"]="eth2") # GPU servers aren't quite consistent, so these might have different "hardware" names
declare -A IF1SD
IF1SD=(["storage"]="enp175s0f0np0" ["gpu"]="eth4") # GPU servers aren't quite consistent, so these might have different "hardware" names

MTU=9000

# Get compute server number
hostname=`hostname`
echo "Hostname is $hostname"

# Get server logical number
# - delimited
IFS="-"
read -a strarr <<< "$hostname"
servernum=${strarr[2]}
servertype=${strarr[1]}

IP=$((${IP_OFFSET[$servertype]} + $servernum))
IP0=${BASEIP0}$IP
IP1=${BASEIP1}$IP

IF0S=${IF0SD[$servertype]}
IF1S=${IF1SD[$servertype]}

for IF0 in ${IF0S[@]};
do
echo "Setting interface $IF0 to $IP0"
ip addr add ${IP0}/24 dev $IF0
# Set MTUs
ip link set mtu $MTU $IF0
# set NIC params
ethtool -s $IF0 speed 100000 autoneg off
# enable interface!
ip link set $IF0 up
done

for IF1 in ${IF1S[@]};
do
echo "Setting interface $IF1 to $IP1"
ip addr add ${IP1}/24 dev $IF1
# Set MTUs
ip link set mtu $MTU $IF1
# set NIC params
ethtool -s $IF1 speed 100000 autoneg off
# enable interface!
ip link set $IF1 up
done
```
