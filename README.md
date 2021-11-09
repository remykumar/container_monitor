# container_monitor
A python program/software that collects monitoring data of the containers running on a host and stores them in AWS mysql database. To be precise, the program collects the configuration of the containers and monitors the CPU & Memory metrics. The data is pushed as html page to nginx server to view on a browser. 
There is a build script also provided in the repo. 

**To execute the monitor as a continuous background daemon process, run it as:**
 
`./build_run_script.sh`

Note : This will collect metrics every 90 seconds and update the mysql database in AWS 

Expected Output: 
```
Synchronizing state of nginx.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable nginx

Container Monitoring Started!

-------------------------------------------------------------------------

Please access the Container Monitoring Portal page here :

http://3.21.129.212/container_monitor.html
```
![image](https://user-images.githubusercontent.com/38254327/140845944-3fe6e056-8b6c-4ef0-886d-80cd763e5b4a.png)





**To execute as foreground process & see , run it as:**

`python3 containers_monitor.py`

Note : This will collect metrics every 90 seconds and update the mysql database in AWS 

Expected Output: 
```
ubuntu@ip-172-31-43-41:~/database_projects/sqllite/container_monitor$ python3 containers_monitor.py

containers table already exists, removing it before creating a fresh copy


CREATED containers table


Number of Container(s) running = 3


COLLECTING STATS FROM RUNNING CONTAINER AND INSERTING INTO DB....


CONTAINER INFO INSERTED INTO THE DATABASE!


GETTING THE DATA FROM containers table:



Image_Name| IP     | CMD    | CPU_Set|CPU_Usage|Memory_Set|Memory_Usage
+---------+---+----+--------+----------+-----------+-------------+
busybox| 172.17.0.2| sleep 500| 250m| 0.00%| 10MiB| 5.16%
busybox| 172.17.0.3| sleep 500| 350m| 0.00%| 20MiB| 1.35%
busybox| 172.17.0.4| dd if=/dev/urandom| 300m| 27.26%| 25MiB| 1.12%
+---------+---+----+--------+----------+-----------+-------------+
```
 

