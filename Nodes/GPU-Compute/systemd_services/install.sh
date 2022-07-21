#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	cp ./hpdaq*.service /etc/systemd/system/
	cp ./redis_gateway.service /etc/systemd/system/
	cp ./hpdaq_service.conf /home/cosmic
	cp ./redis_gateway_service.conf /home/cosmic

	systemctl disable hpdaq
	systemctl disable redis_gateway
	systemctl daemon-reload
	systemctl enable hpdaq
	systemctl enable redis_gateway
fi
