username='root'
password='labdatabase'
import MySQLdb
db=MySQLdb.connect("localhost",username,password,"mysql");
c=db.cursor();
db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
c=db.cursor();
def checkLogin(user_id,user_password):
	db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
	c=db.cursor();
	query = "select count(*) from userinfo where email= '%s' and password = '%s'" % (user_id, user_password )
	print query
	status= (c.execute(query))
	result=c.fetchall()
	print status
	return result[0][0]