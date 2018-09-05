import mysql.connector
import os

connection = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST', '127.0.0.1'),
  user=os.getenv('MYSQL_USER', 'root'),
  passwd=os.getenv('MYSQL_PASS', 'password'),
  database=os.getenv('MYSQL_NAME', 'pegasus'),
)

cursor = pegasus.cursor()

sql = "INSERT INTO currencies (name) VALUES (%s)"
val = ("John",)
cursor.execute(sql, val)

connection.commit()

cursor.close()
connection.close()
