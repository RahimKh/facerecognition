import mysql.connector
import numpy as np


'''mydb = mysql.connector.connect(
  host="https://newnorm.sagecity.io/",
  port=3306,
  user='root',
  password='wqtqVSROVpdhilqI00',
  database='newNorm',
)'''

mydb = mysql.connector.connect(
  host="localhost",
  user="rahim",
  password="123456789",
  auth_plugin='mysql_native_password',
  database="mydatabase"
)

def insert_to_base(id,img_encoded,table):
  try:
    mycursor = mydb.cursor()
    #sql = "INSERT INTO image_vectorielle (user_id, value) VALUES (%s, %s)"
    sql = "INSERT INTO " +table+ " (user_id, value) VALUES (%s, %s)"
    list = img_encoded.tolist()
    val=[(id,v) for v in list[0]]
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
    mycursor.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    return False

def get_encoded_img(id,table):
  try:
    #sql="SELECT value FROM image_vectorielle WHERE user_id="+id
    sql="SELECT value FROM "+table+" WHERE user_id="+id
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    list_values=[item for t in myresult for item in t]
    encoded=np.array(list_values)
    encoded=encoded[np.newaxis,:]
    return encoded
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    return False
  
