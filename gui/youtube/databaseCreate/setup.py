username='root'
password='labdatabase'
import MySQLdb
db=MySQLdb.connect("localhost",username,password,"mysql");
c=db.cursor();
c.execute("DROP database if exists  mytube_main_db");
c.execute("create database mytube_main_db");
db=MySQLdb.connect("localhost",username,password,"mytube_main_db");
c=db.cursor();
c.execute("CREATE TABLE userinfo ( firstname varchar(255) NOT NULL,lastname varchar(255) NOT NULL,gender varchar(255) not null,age varchar(255) NOT NULL,email varchar(255) NOT NULL,password varchar(255) NOT NULL,PRIMARY KEY (email));");

c.execute("CREATE TABLE non_signed_history ( video_id varchar(255) NOT NULL primary key ,view_count int NOT NULL);");

#c.execute("CREATE TABLE userinfo ( userid int ,username varchar(255)),password varchar(255))");
