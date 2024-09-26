import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from mysql.connector.connection import MySQLConnection
import numpy as np


'''mydb = mysql.connector.connect(
  host="https://newnorm.sagecity.io/",
  port=3306,
  user='root',
  password='wqtqVSROVpdhilqI00',
  database='newNorm',
)'''

mydb = mysql.connector.pooling.MySQLConnectionPool(
  pool_name="newnorm_pool",
  pool_size=5,
  pool_reset_session=True,
  host="localhost",
  user="rahim",
  password="123456789",
  auth_plugin='mysql_native_password',
  database="mydatabase"
)

def insert_to_base(id,img_encoded,table):
  try:
    connection_object = mydb.get_connection()
    if connection_object.is_connected():
      mycursor = connection_object.cursor()
      #sql = "INSERT INTO image_vectorielle (user_id, value) VALUES (%s, %s)"
      sql = "INSERT INTO " +table+ " (user_id, value) VALUES (%s, %s)"
      list = img_encoded.tolist()
      val=[(id,v) for v in list[0]]
      mycursor.executemany(sql, val)
      connection_object.commit()
      print(mycursor.rowcount, "was inserted.")
      mycursor.close()
      connection_object.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    return False

def get_encoded_img(id,table):
  try:
    connection_object = mydb.get_connection()
    if connection_object.is_connected():
      mycursor = connection_object.cursor()
      #sql="SELECT value FROM image_vectorielle WHERE user_id="+id
      sql="SELECT value FROM "+table+" WHERE user_id="+id
      mycursor.execute(sql)
      myresult=mycursor.fetchall()
      list_values=[item for t in myresult for item in t]
      encoded=np.array(list_values)
      encoded=encoded[np.newaxis,:]
      mycursor.close()
      connection_object.close()
      return encoded
  except Error as e :
    print ("Error while connecting to MySQL using Connection pool ", e)
    return False
  
if __name__ == "__main__":
  
    db_Info = connection_object.get_server_info()
    print("Connected to MySQL database using connection pool ... MySQL Server version on ",db_Info)
  
  #mycursor.execute(sql)
  #myresult=mycursor.fetchall()
  #print('list'+str(myresult))