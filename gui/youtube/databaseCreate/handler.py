username='root'
password='labdatabase'
import MySQLdb
db=MySQLdb.connect("localhost",username,password,"mysql");
c=db.cursor();
db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
c=db.cursor();
data=[]
def user_registration(l):
	# print type(int(l[3]))
	# print (l[0],l[1],l[2],int(l[3]),l[4],l[5])
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
	c=db.cursor();
	query=" select count(*) from userinfo where email= '%s' " %(l[4])
	print query
	status=c.execute(query)
	result=c.fetchall()
	print status,result
	if result[0][0]:
		return 0
	c.execute("insert into userinfo values (%s,%s,%s,%s,%s,%s)", (l[0],l[1],l[2],str(l[3]),l[4],l[5]));
	c.execute("commit");
	# create a database for user correspoding to email
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	#c.execute("DROP database if exists %s" % l[4]);
	c.execute("create database if not exists %s" % l[4]);
	db=MySQLdb.connect("localhost",username,password,l[4]);
	c=db.cursor();
	# create user_detail table for each user
	table1=l[4]+'_detail'
	c.execute("CREATE TABLE if not exists %s ( firstname varchar(255) NOT NULL,lastname varchar(255) NOT NULL,gender varchar(255) not null,age varchar(255) NOT NULL,email varchar(255) NOT NULL,password varchar(255) NOT NULL,PRIMARY KEY (email));" % table1);
	c.execute("commit");

	# create user_history table
	table2 = l[4]+"_history"
	c.execute("CREATE TABLE if not exists %s ( name varchar(255) NOT NULL primary key , view_count int NOT NULL )" % table2);
	c.execute("commit");

	# create user_bookmark table
	table3 = l[4]+"_bookmark"
	c.execute("CREATE TABLE if not exists %s ( name varchar(255) NOT NULL)" % table3);
	c.execute("commit");

	table4 = l[4]+"_watch_later"
	c.execute("CREATE TABLE if not exists %s ( name varchar(255) NOT NULL)" % table4);
	c.execute("commit");
	return 1

def row(email):
	db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
	c=db.cursor();
	del data[:]
	global data
	c.execute("select * from userinfo where email=%s", [email]);
	data = c.fetchall ();
	return data

def add_history(email,video_id):
	db=MySQLdb.connect("localhost",username,password,email);
	c=db.cursor();
	table1 = email+"_history"
	query ="select * from %s where name= '%s'" % (table1,video_id)
	status=c.execute(query)
	if status:
		query="select view_count from %s where name= '%s'" % (table1,video_id)
		view_count=c.execute(query)
		data=c.fetchall();
		view_count=int(data[0][0])+1
		# query="update into %s where name= '%s' set view_count= %d " %(table1,video_id,view_count)
		query="update "+ table1+ " set view_count= %d" %view_count +" where name= '"+video_id+"'"
		print query
	else:
		query="insert into %s values('%s',%d)"%(table1,video_id,1)
	result=c.execute(query)

	# query = "insert into "+table1+" (name) values ('%s')" % video_id
	# #print query
	# c.execute(query);
	# # c.execute("insert into %s (name) values (%s)" , (table1, name));
	c.execute("commit");

def add_bookmark(email,video_id):
	db=MySQLdb.connect("localhost",username,password,email);
	c=db.cursor();
	table1 = email+"_bookmark"
	query = "insert into "+table1+" (name) values ('%s')" % video_id
	#print query
	c.execute(query);
	c.execute("commit");

def add_watch_later(email,video_id):
	db=MySQLdb.connect("localhost",username,password,email);
	c=db.cursor();
	table1 = email+"_watch_later"
	query = "insert into "+table1+" (name) values ('%s')" % video_id
	#print query
	c.execute(query);
	c.execute("commit");


def non_signed_history(video_id):
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
	c=db.cursor();
	query ="select * from non_signed_history where non_signed_history.video_id= '%s'" % (video_id)
	status=c.execute(query)
	if status:
		query="select view_count from non_signed_history where non_signed_history.video_id= '%s'" % (video_id)
		view_count=c.execute(query)
		data = c.fetchall ();
		#print data[0][0]
		# print view_count
		view_count=data[0][0]+1
		#print view_count
		query="update non_signed_history set view_count= %d" %view_count +" where video_id= '"+video_id+"'"
		#print query
		# query="update into non_signed_history where non_signed_history.video_id= '%s' set non_signed_history.view_count= %d " %(video_id,view_count)
	else:
		query="insert into non_signed_history values('%s',%d)"%(video_id,1)
	result=c.execute(query)
	c.execute('commit');
	return 1
	#c.execute("insert into non_signed_history values (%s,%s)");
	#c.execute("commit");

def history(user_id):
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	db=MySQLdb.connect("localhost",username,password,user_id);
	c=db.cursor();
	table_name=user_id+'_history'
	query ="select name from %s " % (table_name)+"order by view_count desc limit 18"
	status=c.execute(query)
	output=c.fetchall()
	return output

def nonHistory():
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
	c=db.cursor();
	table_name='non_signed_history'
	query ="select video_id from %s " % (table_name)+"order by view_count desc limit 18"
	status=c.execute(query)
	output=c.fetchall()
	return output



def search_for_logged_in(video_id,user_id):
	database=user_id
	db=MySQLdb.connect("localhost",username,password,database);
	c=db.cursor();
	table_name=user_id+'_history'
	viewCount=0
	query ="select * from %s where name= '%s'" % (table_name,video_id)
	status=c.execute(query)
	if status:
		query="select view_count from %s where name= '%s'" % (table_name,video_id)
		result=c.execute(query)
		data=c.fetchall();
		viewCount=data[0][0]
	return viewCount
def search_for_not_logged_in(video_id):
	# pass
	database='mytube_main_db'
	db=MySQLdb.connect("localhost",username,password,database);
	c=db.cursor();
	table_name='non_signed_history'
	viewCount=0
	query ="select * from %s where video_id= '%s'" % (table_name,video_id)
	status=c.execute(query)
	if status:
		query="select view_count from %s where video_id= '%s'" % (table_name,video_id)
		result=c.execute(query)
		data=c.fetchall();
		viewCount=data[0][0]
	return viewCount


def user_history(user_id):
	db=MySQLdb.connect("localhost",username,password,"mysql");
	c=db.cursor();
	db=MySQLdb.connect("localhost",username,password,user_id);
	c=db.cursor();
	table_name=user_id+'_history'
	query ="select name from %s " % (table_name)+"order by view_count desc limit 18"
	status=c.execute(query)
	output=c.fetchall()
	return output

