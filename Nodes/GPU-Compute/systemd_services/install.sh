#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	cp ./hpdaq.service /etc/systemd/system/
	cp ./hpdaq_service.conf /home/cosmic

	systemctl disable hpdaq
	systemctl daemon-reload
	systemctl enable hpdaq
fi
