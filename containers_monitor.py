#!/usr/bin/env python3 
import mysql.connector
import os 

# Getting the container count 
container_count = os.popen('docker ps -q | wc -l').read().strip()

if container_count == "0":
 print ("\nNO CONTAINERS RUNNING FOR MONITORING.. EXITING PROGRAM\n")
 exit()


conn = mysql.connector.connect(user='root',password='Password-18',host='database-1.cea7il7mfhry.us-east-2.rds.amazonaws.com',database='test') 
cur = conn.cursor(buffered=True) 

cur.execute("show tables like '%containers%'") 
result = cur.fetchall()
#result = cur.execute("SELECT table_name FROM information_schema.tables where table_name='containers'") 
#print(result)
if result: 
    print ("\ncontainers table already exists, removing it before creating a fresh copy\n")
    cur.execute("drop table containers") 
    conn.commit()


cur.execute('''CREATE TABLE containers
        (Image_Name VARCHAR(20) NOT NULL, 
        IP VARCHAR(20) NOT NULL, 
        CMD VARCHAR(20) NOT NULL,
        CPU_Set VARCHAR(20) NOT NULL,
        CPU_Usage VARCHAR(20) NOT NULL,
        Memory_Set VARCHAR(20) NOT NULL,
        Memory_Usage VARCHAR(20) NOT NULL,
        PRIMARY KEY(IP))
        ''') 

print("\nCREATED containers table\n") 
# Get the count of running containers
container_count = os.popen('docker ps -q | wc -l').read().strip()

if container_count == "0": 
 print ("NO CONTAINERS RUNNING.. EXITING PROGRAM") 
 exit() 

print(f'\nNumber of Container(s) running = {container_count}\n')
print("\nCOLLECTING STATS FROM RUNNING CONTAINER AND INSERTING INTO DB....\n")
container_ids = os.popen('docker ps -q').read() 
for line in container_ids.splitlines(): 
    #print(line)
    try: 
     Image_Name = os.popen('docker inspect '+line+' --format=\'{{.Config.Image}}\'').read().strip()
    except ValueError: 
     print("Could not get the Image_Name - setting it to unknown") 
     Image_Name = "unknown"
    #print(Image_Name)
    try:
     IP = os.popen('docker inspect '+line+' --format=\'{{.NetworkSettings.IPAddress}}\'').read().strip()
    except ValueError: 
     print("Could not get the IP - setting it to X.X.X.X") 
     IP = "X.X.X.X"
    #print(IP)
    try:
     CMD = os.popen('docker inspect '+line+' --format=\'{{.Config.Cmd}}\' | sed -e "s/\[//g" | sed -e "s/\]//g"').read().strip()
    except ValueError: 
     print("Could not get the CMD - setting it to N/A") 
     CMD = "N/A"
    #print(CMD)
    try: 
     CPU_Set = os.popen('docker inspect '+line+' --format=\'{{.HostConfig.NanoCpus}}\' | awk \'{print $1/1000000 "m"}\'').read().strip()
     if CPU_Set == "0m": 
         CPU_Set = "uncapped"
    except ValueError: 
     print("Could not get the CPU_Set - setting it to uncapped") 
     CPU_Set = "uncapped"
    #print(CPU_Set)
    try: 
     CPU_Usage = os.popen('docker stats --no-stream '+line+' | awk \'{print $3}\' | tail -1').read().strip() 
    except ValueError: 
     print("Could not get CPU_Usage - setting it to 0") 
     CPU_Usage = "0" 
    #print(CPU_Usage)a
    try: 
     Memory_Set = os.popen('docker stats --no-stream '+line+' | awk \'{print $6}\' | tail -1').read().strip()
     if Memory_Set == "0MiB": 
         Memort_Set = "uncapped"
    except ValueError: 
     print("Could not get Memory_Set - setting it to uncapped") 
     Memory_Set = "uncapped"
    #print(Memory_Set)
    try: 
     Memory_Usage = os.popen('docker stats --no-stream '+line+' | awk \'{print $7}\' | tail -1').read().strip()
    except ValueError: 
     print("Could not get Memory_Usage - setting it to 0") 
     Memory_Usage = "0"
    #print(Memory_Usage)
    insert_query = """INSERT into containers (Image_Name, IP, CMD, CPU_Set, CPU_Usage, Memory_Set, Memory_Usage) values (%s, %s, %s, %s, %s, %s, %s) """
    record = (Image_Name, IP, CMD, CPU_Set, CPU_Usage, Memory_Set, Memory_Usage)
    cur.execute(insert_query,record)
    #cur.execute("INSERT into containers (Image_Name, IP, CMD, CPU_Set, CPU_Usage, Memory_Set, Memory_Usage) values (%s, %s, %s, %s, %s, %s, %s), (Image_Name, IP, CMD, CPU_Set, CPU_Usage, Memory_Set, Memory_Usage)")
    #cur.execute("INSERT into containers "
    #            "(Image_Name, IP, CMD, CPU_Set, CPU_Usage, Memory_Set, Memory_Usage) " 
    #            "values (%(Image_Name)s, %(IP)s, %(CMD)s, %(CPU_Set)s, %(CPU_Usage)s, %(Memory_Set)s, %(Memory_Usage)s)")

"""
cur.execute("insert into containers values('AAL','American Airlines')")
cur.execute("insert into containers values('UAL','United Airlines')")
cur.execute("insert into containers values('LUV','Southwest Airlines')")
cur.execute("insert into containers values('VA','Virgin America')")
"""
conn.commit() 
#c.execute("select * from stocks")
conn.close() 

print ("\nCONTAINER INFO INSERTED INTO THE DATABASE!\n")

print ("\nGETTING THE DATA FROM containers table:\n")
#table_result = os.popen("containers_read.py").read()
exec(open("containers_read.py").read())
