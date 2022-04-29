import mysql.connector

con = mysql.connector.connect(host='mysql5038.site4now.net',
                              user='a85558_mikiney',
                              password='DpIeCZkBCx1',
                              port=3306,
                              database='db_a85558_mikiney')

if con.is_connected():
    print('Connected')
else:
    print('Not connected')

cur = con.cursor()

# cur.execute('delete from tech_adp')
# con.commit()

cur.execute('describe tech_adp')
for i in cur.fetchall():
    print(i)
print(cur.rowcount)

con.close()
