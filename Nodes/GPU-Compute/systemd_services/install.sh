#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	cp ./hpguppi*.service /etc/systemd/system/
	cp ./redis_gateway.service /etc/systemd/system/
	cp ./init_hpguppi*.sh /usr/local/bin/
	cp ./hpguppi_service.conf /home/cosmic/dev/hpguppi_daq
	cp ./redis_gateway_service.conf /home/cosmic/dev/hpguppi_daq

	systemctl disable hpguppi
	systemctl disable hpguppi_pypeline
	systemctl disable redis_gateway
	systemctl daemon-reload
	systemctl enable hpguppi
	systemctl enable hpguppi_pypeline
	systemctl enable redis_gateway
fi
