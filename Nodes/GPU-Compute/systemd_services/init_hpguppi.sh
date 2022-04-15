#!/bin/bash

export HASHPIPE_KEYFILE=/home/cosmic

instance_systemname=$1
if [ -z "$1" ]
then
  instance_systemname="pktsock_atasnap_optimised"
fi

/home/cosmic/dev/hpguppi_daq/src/init_hpguppi.py $instance_systemname 0,1 --configfile '/home/cosmic/dev/hpguppi_daq/src/config_hpguppi.yml' >> /var/log/init_hpguppi.log 2>&1

#exit 0
