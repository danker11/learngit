import module
import pye
# dbinfo
host='127.0.0.1'
username='steven'
password='modb123$'
port='1888'
dbconn=pyzenith.connect(host,username,password,port)
cursorc=dbconn.cursor()
cursorc.execute("select * from steven_test")
results =cursorc.fetchall()
print(results)
cursorc.close()
dbconn.close()
