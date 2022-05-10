#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	#cp ./init_casperfpga_rest_server.sh /usr/local/bin/
	#cp ./casperfpga_rest_server.service /etc/systemd/system/

	cp ./init_remoteobjects_server.sh /usr/local/bin/
	cp ./remoteobjects_server.service /etc/systemd/system/

	#systemctl disable casperfpga_rest_server
	systemctl disable remoteobjects_server
	systemctl daemon-reload
	#systemctl enable casperfpga_rest_server
	systemctl enable remoteobjects_server
fi
