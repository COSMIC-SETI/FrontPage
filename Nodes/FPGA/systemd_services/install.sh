#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else

	cp ./remoteobjects_server.service /etc/systemd/system/
	cp ./remoteobjects_server.conf /home/cosmic

	systemctl disable remoteobjects_server
	systemctl daemon-reload
	systemctl enable remoteobjects_server
fi
