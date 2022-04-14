#!/bin/bash 

if [[ $EUID > 0 ]]
then 
  echo "Please run with super-user privileges"
  exit 1
else
	cp ./redis_server.service /etc/systemd/system/
	cp ./init_redis_server.sh /usr/local/bin/

	systemctl disable redis_server
	systemctl daemon-reload
	systemctl enable redis_server

fi