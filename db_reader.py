#!/usr/bin/env python3
import sqlite3
import mysql.connector
import os 

#conn = sqlite3.connect('testdb.db')
user = os.popen('cat /home/ubuntu/.secret.txt | grep user | awk -F "=" \'{print $2}\'').read().strip()
password = os.popen('cat /home/ubuntu/.secret.txt | grep password | awk -F "=" \'{print $2}\'').read().strip()
host = os.popen('cat /home/ubuntu/.secret.txt | grep host | awk -F "=" \'{print $2}\'').read().strip()
database = os.popen('cat /home/ubuntu/.secret.txt | grep "database=" | awk -F "=" \'{print $2}\'').read().strip()
conn = mysql.connector.connect(user=''+user+'',password=''+password+'',host=''+host+'',database=''+database+'')
c = conn.cursor()

c.execute("select * from containers")
results = c.fetchall()
print ('\n')
print (f'Image_Name| IP     | CMD    | CPU_Set|CPU_Usage|Memory_Set|Memory_Usage') 
print (f'+---------+---+----+--------+----------+-----------+-------------+')
res = []
if results:
    for r in results:
        #print (r.replace("(","").replace(",", "|").replace("'",""))
        res.append(r)
#res_string = str(res).replace("(","").replace(")","").replace("'","")
dataline="<table><tr><td style=color:beige>Image_Name</td><td style=color:beige>IP</td><td style=color:beige>CMD</td><td style=color:beige>CPU_Set</td><td style=color:beige>CPU_Usage</td><td style=color:beige>Memory_Set</td><td style=color:beige>Memory_Usage</td>"

for i in res: 
 res_string = str(i).replace("(","").replace(")","").replace(",","|").replace("'","")
 dataline = dataline+"<tr>"
 for word in res_string.split("|"): 
  dataline = dataline+"<td style=color:salmon>"+word+"</td>"
 dataline = dataline+"</tr>" 
 print (res_string)
dataline=dataline+"</table>"
print (f'+---------+---+----+--------+----------+-----------+-------------+\n')
conn.close()


# Get the current system time
currTime = os.popen('date').read().strip()

"""
dataline="<table>"
for line in res_string.splitlines():
  #print(line)
  dataline = dataline+"<tr>"
  for word in line.split(","):
   #print(word)
   dataline = dataline+"<td style=color:red>"+word+"</td>"
  dataline = dataline+"</tr>"
dataline=dataline+"</table>"
"""
# Create the container monitor html  file and open it for write
stats_file="container_monitor.html"
os.system('touch '+stats_file+'')
outfile = open(stats_file, 'w')

outfile.write('<html><head><meta http-equiv="refresh" content="90"></head><style>table { width:100%;} table, th, td { border: 1px solid white;} th, td {padding: 9px;text-align: left;} th {background-color: darkred;color: white;}</style><table>')
outfile.write('<body style="background-color:black;"><h2 style="background-color:beige;"><p style="text-align:center;">Container Real time Monitoring Portal</p></h2>')
outfile.write("\n")
#outfile.write('<tr><th><h2>Image_Name</h2></th><th><h2>IP</h2></th><th><h2>CMD</h2></th><th><h2>CPU_Set</h2></th><th><h2>CPU_Usage</h2></th><th><h2>Memory_Set</h2></th><th><h2>Memory_Usage</h2></th></tr>')
outfile.write("\n")
outfile.write(f'{dataline}')
outfile.write(f'<h4><p style="color:beige;">Data last polled @ {currTime}</p></h4><h4><p style="color:dimgray;">Note : Page refreshes every 90 seconds to update latest stats</p></h4></body></html>')
outfile.close()

os.system('sudo cp container_monitor.html /var/www/html/') 
