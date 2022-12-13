
import mysql.connector

# custom modules
import config as configs

mydb = mysql.connector.connect(
  host= configs.db_server,
  user= configs.db_username,
  password= configs.db_password,
  database= configs.db_name
)

mycursor = mydb.cursor()


def tabChange(tabIndex):

  sql = "UPDATE table1 SET column1 = "+"'"+str(tabIndex)+"'"

  mycursor.execute(sql)

  mydb.commit()

  # return mycursor.rowcount, "command executed"

