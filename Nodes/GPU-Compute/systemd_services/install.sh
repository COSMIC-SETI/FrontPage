#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	cp ./nvidia_power_limit.service /etc/systemd/system/
	cp ./hpdaq*.service /etc/systemd/system/
	cp ./hpdaq_service.conf /home/cosmic

	systemctl disable nvidia_power_limit
	systemctl disable hpdaq
	systemctl disable hpdaq_secondary
	systemctl daemon-reload
	systemctl enable nvidia_power_limit
	systemctl enable hpdaq
	systemctl enable hpdaq_secondary
fi
