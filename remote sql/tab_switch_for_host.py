import mysql.connector
from time import sleep

# custom modules

import config as configs

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from selenium import webdriver
driver = webdriver.Chrome (executable_path="C:\chromedriver\chromedriver.exe")





try:

    mydb = mysql.connector.connect(
    host= configs.db_server,
    user= configs.db_username,
    password= configs.db_password,
    database= configs.db_name
    )

    mycurser = mydb.cursor()
    mycurser.execute("select * from table2")

    symbols_list = mycurser.fetchall()
    mycurser.close()
except:
    print("error in sql while connecting to table2")

symbols_list = str(symbols_list[0][0])

symbols_list = symbols_list.split(", ")
symbols_list.pop()



driver.get("https://pro.upstox.com")

input("press enter to start adding tabs")

for symbol in symbols_list:
    
    search_bar = driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/section/div/div[1]/div/div[1]/div/cq-context/div[1]/div[2]/div/div[1]")
    search_bar.click()
    sleep(8)
    driver.find_element_by_xpath('//*[@id="iq_chart_container"]/div[1]/div/cq-context/div[1]/div[2]/div[1]/div/div[1]/div/div/div/input').send_keys(symbol)
    sleep(8)
    first_row = driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/section/div/div[1]/div/div[1]/div/cq-context/div[1]/div[2]/div[1]/div/div[3]/div/div")
    first_row.click()
    driver.execute_script("window.open('https://pro.upstox.com');")
    sleep(8)





input("press enter to listen db tab changes")
# variables to debug
tabIndex = 0

# other variables
dataReceivedStored = "NIL"


while True:

    try:

        mydb = mysql.connector.connect(
        host= configs.db_server,
        user= configs.db_username,
        password= configs.db_password,
        database= configs.db_name
        )

        mycurser = mydb.cursor()
        mycurser.execute("select * from table1")

        result = mycurser.fetchall()
    
    except:
        print("error in sql while connecting to table1")

    try:

        dataReceived = (result[0][0])

        if dataReceived == "0" and dataReceivedStored != "0":
            tabIndex = 0
            driver.switch_to.window(driver.window_handles[0])

        elif dataReceived == "1" and dataReceivedStored != "1":
            tabIndex = 1
            driver.switch_to.window(driver.window_handles[1])

        elif dataReceived == "2" and dataReceivedStored != "2":
            tabIndex = 2
            driver.switch_to.window(driver.window_handles[2])

        elif dataReceived == "3" and dataReceivedStored != "3":
            tabIndex = 3
            driver.switch_to.window(driver.window_handles[3])

        elif dataReceived == "4" and dataReceivedStored != "4":
            tabIndex = 4
            driver.switch_to.window(driver.window_handles[4])

        elif dataReceived == "5" and dataReceivedStored != "5":
            tabIndex = 5
            driver.switch_to.window(driver.window_handles[5])

        elif dataReceived == "6" and dataReceivedStored != "6":
            tabIndex = 6
            driver.switch_to.window(driver.window_handles[6])

        elif dataReceived == "7" and dataReceivedStored != "7":
            tabIndex = 7
            driver.switch_to.window(driver.window_handles[7])

        elif dataReceived == "8" and dataReceivedStored != "8":
            tabIndex = 8
            driver.switch_to.window(driver.window_handles[8])

        elif dataReceived == "9" and dataReceivedStored != "9":
            tabIndex = 9
            driver.switch_to.window(driver.window_handles[9])

        elif dataReceived == "10" and dataReceivedStored != "10":
            tabIndex = 10
            driver.switch_to.window(driver.window_handles[10])

        elif dataReceived == "11" and dataReceivedStored != "11":
            tabIndex = 11
            driver.switch_to.window(driver.window_handles[11])

        elif dataReceived == "12" and dataReceivedStored != "12":
            tabIndex = 12
            driver.switch_to.window(driver.window_handles[12])

        elif dataReceived == "13" and dataReceivedStored != "13":
            tabIndex = 13
            driver.switch_to.window(driver.window_handles[13])

        elif dataReceived == "14" and dataReceivedStored != "14":
            tabIndex = 14
            driver.switch_to.window(driver.window_handles[14])

        elif dataReceived == "15" and dataReceivedStored != "15":
            tabIndex = 15
            driver.switch_to.window(driver.window_handles[15])

        elif dataReceived == "16" and dataReceivedStored != "16":
            tabIndex = 16
            driver.switch_to.window(driver.window_handles[16])

        elif dataReceived == "17" and dataReceivedStored != "17":
            tabIndex = 17
            driver.switch_to.window(driver.window_handles[17])

        elif dataReceived == "18" and dataReceivedStored != "18":
            tabIndex = 18
            driver.switch_to.window(driver.window_handles[18])

        elif int(dataReceived) > 18:
            print("not in range 0 - 18")



    except:
        print("error while switching to tab: ", tabIndex)

    dataReceivedStored = dataReceived