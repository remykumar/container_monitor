#!/bin/bash


# nginx server : starting/enabling it 
sudo systemctl start nginx
sudo systemctl enable nginx

# Get the internal and external IP of the host machine
INT_IP=`hostname -I | awk '{print $1}'`
EXT_IP=`curl -s api.ipify.org`

# curl the External and Internal IP addresses to check the 200 success status. Use External first since this code is to be run on AWS EC2 instance
FINAL_URL=""
RESP=`curl -s -I http://$EXT_IP/container_monitor.html --connect-timeout 3 | grep HTTP | grep OK`

if [[ -z $RESP ]]; then
 RESP=`curl -s -I http://$INT_IP/container_monitor.html --connect-timeout 3 | grep HTTP | grep OK`
 if [[ -z $RESP ]]; then
  echo -e "\n!!! Monitor Deploy not successful - Site not reachable!!!!. \nPossible reasons could be :\n
         1. Http server is not running \n
         2. Internet is not working or network issues \n
         3. Firewall blocking port 80 \n"
  exit
 else
 FINAL_URL=http://$INT_IP/container_monitor.html
 fi
else
 FINAL_URL=http://$EXT_IP/container_monitor.html
fi

echo -e "\nContainer Monitoring Started!\n"
sleep 2
echo -e "-------------------------------------------------------------------------\n"
echo -e "Please access the Container Monitoring Portal page here : \n"
echo -e "$FINAL_URL\n"

# Make sure the existing instance of python instance (if running) is killed and new one is started
echo -en "\nBuilding the code ."
PID=`pgrep -f containers_monitor.py`
if [ -z $PID ]; then
	 nohup python3 containers_monitor.py 2>/dev/null &
 else
	  kill -9 $PID
	  nohup python3 containers_monitor.py 2>/dev/null & 
fi

