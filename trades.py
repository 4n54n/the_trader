
import mysql.connector

# custom modules
import config as configs






tradeList = {

        "SBIN-EQ":3045,
        "ZOMATO-EQ":5097,
        "HINDALCO-EQ":1363,
        "GRASIM-EQ":1232,
        "TATACOMM-EQ":3721,
        "HCLTECH-EQ":7229,
        "INFY-EQ":1594,
        "ADANIPORTS-EQ":15083,
        "APOLLOHOSP-EQ":157,
        "HDFCLIFE-EQ":467,
        "BRITANNIA-EQ":547,
        "BAJAJFINSV-EQ":16675,
        "RELIANCE-EQ":2885,
        "HDFCBANK-EQ":1333,
        "BAJFINANCE-EQ":317,
        "HDFC-EQ":1330,
        "ASIANPAINT-EQ":236,
        "ICICIBANK-EQ":4963
        
}


# To sync to the online db ( database1, table2, column1)

symbols_sep = ""
for key in tradeList.keys():
        symbols_sep += key.replace("-EQ", " NSE EQ")+", "

print(symbols_sep)


mydb = mysql.connector.connect(
  host= configs.db_server,
  user= configs.db_username,
  password= configs.db_password,
  database= configs.db_name
)

mycursor = mydb.cursor()

sql = mycursor.execute("UPDATE table2 SET column1 = "+"'"+str(symbols_sep)+"';")
mydb.commit()
print(mycursor.rowcount, "command executed")

