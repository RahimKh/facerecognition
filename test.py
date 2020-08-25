import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="localhost",
  user="rahim",
  password="123456789",
  auth_plugin='mysql_native_password',
  database="mydatabase"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("CREATE TABLE imagevecteurielle  (id INT AUTO_INCREMENT , user_id INT , value DOUBLE ,PRIMARY KEY(id,user_id) )")

sql="SELECT value FROM encoding1 WHERE user_id=753"
mycursor.execute(sql)
myresult=mycursor.fetchall()
print(myresult)
list_values=[item for t in myresult for item in t]
encoded=np.array(list_v)
print(encoded.shape)
#encoded=encoded[np.newaxis,:]