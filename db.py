import sqlite3
from datetime import date

conn = sqlite3.connect('database.db')
c = conn.cursor()
today = str(date.today())


backupFound = False
dataFound = False
backupDate = ""


# TABLES : info, orderdata, log, colornote


def updb_orderdata(symbol, quantity, buysell):

    check = c.execute("SELECT * FROM orderdata WHERE symbol = '"+str(symbol)+"';").fetchall()
    if check != []:
        c.execute("UPDATE orderdata SET quantity = '"+str(quantity)+"', buysell= '"+str(buysell)+"' WHERE symbol = '"+str(symbol)+"';")

    else:
        c.execute('''INSERT INTO orderdata VALUES(?,?,?);''', (str(symbol), str(quantity), str(buysell)))
        
    conn.commit()

def delete_orderdata(symbol):
    c.execute("DELETE FROM orderdata WHERE symbol = '"+str(symbol)+"';")
    conn.commit()

def updb_log(log):
    check = c.execute('''SELECT * FROM log''').fetchall()
    if check != []:
        c.execute('''DELETE FROM log;''')
    c.execute('''INSERT INTO log VALUES(?);''', (str(log),))
    conn.commit()


def updb_colornote(symbol, color):

    if color != "white":

        check = c.execute("SELECT * FROM colornote WHERE symbol = '"+str(symbol)+"';").fetchall()

        if check != []:
            c.execute("UPDATE colornote SET color = '"+str(color)+"' WHERE symbol = '"+str(symbol)+"';")
        else:
            c.execute('''INSERT INTO colornote VALUES(?,?);''', (str(symbol), str(color)))

    if color == "white":
        check = c.execute("SELECT * FROM colornote WHERE symbol = '"+str(symbol)+"';").fetchall()

        if check != []:
            c.execute("DELETE FROM colornote WHERE symbol = '"+str(symbol)+"';")

    conn.commit()


def close_db():
    conn.close()

def fetch_backup():

    if backupFound == True:
        global orderdata_TableData, log_TableData, colornote_TableData

        if orderdata_TableData == []:
            orderdata_TableData = False
        if log_TableData == []:
            log_TableData = False
        if colornote_TableData == []:
            colornote_TableData = False

        if orderdata_TableData != False or log_TableData != False or colornote_TableData != False:
            return backupDate, orderdata_TableData, log_TableData, colornote_TableData

        else:
            return False


def clear_backup():
    c.execute('''DELETE FROM orderdata;''')
    c.execute('''DELETE FROM log;''')
    c.execute('''DELETE FROM colornote;''')
    conn.commit()







def isInfoTable():
    isinfo = c.execute(" SELECT name FROM sqlite_master WHERE type='table' AND name='info'; ").fetchall()
    return isinfo

isInfoTable()



# do nothing for new database, delete all table if date is not today
if isInfoTable() != []:

    infoTableData = c.execute("""SELECT * FROM info;""").fetchall()
    
    if infoTableData !=[]:
        backupDate = infoTableData[0][0]
        if backupDate != today:
            c.execute('''DROP TABLE IF EXISTS info;''')
            c.execute('''DROP TABLE IF EXISTS orderdata;''')
            c.execute('''DROP TABLE IF EXISTS log;''')
            c.execute('''DROP TABLE IF EXISTS colornote;''')
            conn.commit()



isInfoTable()

# fetch all the data of todays db

if isInfoTable() != []:
    info_TableData = c.execute("""SELECT * FROM info;""").fetchall()
    
    if info_TableData !=[]:

        backupFound = True
        backupDate = infoTableData[0][0]


    # continue fetching all the tables

    orderdata_TableData = c.execute('''SELECT * FROM orderdata;''').fetchall()
    log_TableData = c.execute('''SELECT * FROM log;''').fetchall()
    colornote_TableData = c.execute('''SELECT * FROM colornote;''').fetchall()





# create tables if it's new run for today
else:

    c.execute('''CREATE TABLE info(date VARCHAR);''')
    c.execute('''INSERT INTO info VALUES(?);''', (today,))
    conn.commit()


    c.execute('''CREATE TABLE orderdata(symbol VARCHAR, quantity INT, buysell VARCHAR);''')
    c.execute('''CREATE TABLE log(log1 TEXT);''')
    c.execute('''CREATE TABLE colornote(symbol VARCHAR, color VARCHAR);''')
    conn.commit()

