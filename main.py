from pyautogui import sleep
from smartapi import SmartConnect

# import custom modules
from trades import tradeList
import config as configs
from sql_tab_switcher import tabChange
import db

import pyotp

import tkinter as tk
from tkinter import *
from tkinter import ttk

import threading
import os
from playsound import playsound

import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')




win = tk.Tk()
win.geometry("1785x935")
canvas = tk.Canvas(win, height=935, width=1750)

win.title("THE TRADER")




# RESTORE POPUP START



backup = False

backupdata = db.fetch_backup()


if backupdata != False:
    backup = True

    try:
        backupdate = backupdata[0]
    except:
        backupdata = db.fetch_backup()
        backupdate = backupdata[0]

    orderdata = backupdata[1]
    log = backupdata[2]
    colornote = backupdata[3]



def restoreBackup():
    global orderdata_var, log_var, colornote_var
    try:
        orderdata_var = orderdata_var.get()
    except:
        orderdata_var = 0
    try:
        log_var = log_var.get()
    except:
        log_var = 0
    try:
        colornote_var = colornote_var.get()
    except:
        colornote_var = 0


    # restore start



    if orderdata_var == 1:
        global stockExec, rule
        for orders in orderdata:

            
            if orders[0] in tradeList.keys():

                stockExec(orders[0], orders[1], 0, orders[2]) # here '0' means don't execute order.

        rule = "buy" # reset the rule to default


    if log_var == 1:
        global log_section
        log_section.insert(END, log[0][0])



    if colornote_var == 1:
        global colorCodeDict
        for colordata in colornote:
            
            if colordata[0] in tradeList.keys():
                canvas.itemconfig(colorCodeDict[colordata[0]], fill= colordata[1])
        



    if orderdata_var == 0 and log_var == 0 and colornote_var == 0:
    
        db.clear_backup()




    # restore end


    top.destroy()


def on_closing_top():
    exit()

def deleteIgnore():
    db.clear_backup()
    top.destroy()

if backup == True:
    top= Toplevel(win)
    

    # make restore popup focused
    top.grab_set()
    # top.focus()

    # set geometry

    top.geometry('%dx%d+%d+%d' % (750, 250, (top.winfo_screenwidth()/2) - (750/2), (top.winfo_screenheight()/2) - (250/2)))




    Label(top, text= "Backup Found - "+backupdate, font=('Helvetica 14 bold')).place(x=150,y=10)

    if orderdata != False:
        global orderdata_var
 
        orderdata_var = IntVar()
        Checkbutton(top, text="order data", font=('Helvetica 11'), height=1, variable=orderdata_var).place(x=150,y=80)

    if log != False:


        log_var = IntVar()
        Checkbutton(top, text="log", font=('Helvetica 11'), height=1, variable=log_var).place(x=150,y=120)

    if colornote != False:

        colornote_var = IntVar()
        Checkbutton(top, text="color data", font=('Helvetica 11'), height=1, variable=colornote_var).place(x=150,y=160)

    Button(top, bg= "green", foreground= "white", text= "RESTORE", font=('Helvetica 10'), height= 1, command= restoreBackup).place(x=400, y=150)
    Button(top, bg= "red", foreground= "white", text= "DELETE and IGNORE", font=('Helvetica 10'), height= 1, command= deleteIgnore).place(x=500, y=150)
    



    top.protocol("WM_DELETE_WINDOW", on_closing_top)


# RESTORE POPUP END



# SCHEDULE WINDOW START


def open_schedule_win():
    schedule_top= Toplevel(win)
    



    # make window focused
    schedule_top.grab_set()
    # schedule_top.focus()

    # set geometry
    schedule_top.geometry('%dx%d+%d+%d' % (1000, 400, (schedule_top.winfo_screenwidth()/2) - (750/2), (schedule_top.winfo_screenheight()/2) - (250/2)))

    
    warning_label = StringVar()
    Label(schedule_top, text= "Schedule", font=('Helvetica 14 bold')).place(x=450, y=10)
    Label(schedule_top, textvariable = warning_label, font=('Helvetica 10')).place(x=750, y=12)
    Button(schedule_top, text="ADD", bg= "yellow", command= lambda:add_schedule()).place(x=480, y=100)
    Button(schedule_top, text="DELETE", bg= "red", fg= "white", command= lambda:delete_schedule()).place(x=845, y=100)


    task_id_clicked = StringVar()

    task_id_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = task_id_clicked)
    task_id_combobox.pack()
    task_id_combobox.place(x= 700, y= 105)
    task_id_combobox.set("choose")

    
    scheduled_data_textarea = Text(schedule_top, background="#001755", foreground="white", width= 86, height=10)
    scheduled_data_textarea.pack()
    scheduled_data_textarea.place(x=45, y=150)


    

# >>>>>>>>>>>>>>>>>>>>>>

    schedule_data = []

# >>>>>>>>>>>>>>>>>>>>>>

# FUNCTIONS


    def show_tasks():
        count = 0
        count_list = []

        scheduled_data_textarea.delete("1.0", "end")
        for data in schedule_data:
            
            scheduled_data_textarea.insert(END, f"ID : {count}      {data}\n")
            count_list.append(count)
            count += 1
        task_id_combobox["values"] = count_list
    

    def delete_schedule():
        global task_id
        try:
            task_id = int(task_id_combobox.get())
        except:
            warning_label.set("Choose ID to delete")
            return None
        if task_id < len(schedule_data) and task_id >= 0:
            schedule_data.pop(task_id)
            show_tasks()
        else:
            warning_label.set("invalid ID")


    def add_schedule():

        main_selected = main_combobox.get()
        sub_a_selected = sub_a_combobox.get()
        sub_b_selected = sub_b_combobox.get()
        sub_c_selected = sub_c_combobox.get()
        sub_d_selected = sub_d_combobox.get()
        sub_e_selected = sub_e_combobox.get()
        


        if main_selected == "symbol":
            warning_label.set("")

            process_symbol = True

            if sub_a_selected not in all_symbols:
                warning_label.set("select box 2")
                process_symbol = False

            if sub_b_selected not in ["ltp <=", "ltp >=", "point >=", "diff >="]:
                warning_label.set("select box 3")
                process_symbol = False

            try:
                int(sub_c_selected)
            except:
                warning_label.set("box 4 is not a number")
                process_symbol = False

            if sub_d_selected not in ["buy", "sell", "alarm"]:
                warning_label.set("select box 5")
                process_symbol = False
            
            # box e(6)
            if sub_d_selected == "alarm":
                if sub_e_selected not in alarmTunes:
                    warning_label.set("select box 6")
                    process_symbol = False

            if sub_d_selected == "buy" or sub_d_selected == "sell":
                try:
                    int(sub_e_selected)
                except:
                    warning_label.set("box 6 is not a number")
                    process_symbol = False
            
            if process_symbol == True:

                toUpdate = [main_selected, sub_a_selected, sub_b_selected, sub_c_selected, sub_d_selected, sub_e_selected]
                if toUpdate not in schedule_data:
                    schedule_data.append(toUpdate)
                    show_tasks()
                    warning_label.set("")
                else:
                    warning_label.set("WARNING : task already added")



        elif main_selected == "order":
            warning_label.set("")

            process_order = True

            if sub_a_selected not in ordered_symbols:
                warning_label.set("select box 2")
                process_order = False

            if sub_b_selected not in ["ltp <=", "ltp >=", "gainloss <=", "gainloss >=", "point >=", "diff >="]:
                warning_label.set("select box 3")
                process_order = False

            try:
                int(sub_c_selected)
            except:
                warning_label.set("box 4 is not a number")
                process_order = False

            if sub_d_selected not in ["buy", "sell", "alarm"]:
                warning_label.set("select box 5")
                process_order = False
            
            # box e(6)
            if sub_d_selected == "alarm":
                if sub_e_selected not in alarmTunes:
                    warning_label.set("select box 6")
                    process_order = False

            if sub_d_selected == "buy" or sub_d_selected == "sell":
                try:
                    int(sub_e_selected)
                except:
                    warning_label.set("box 6 is not a number")
                    process_order = False
            
            if process_order == True:

                toUpdate = [main_selected, sub_a_selected, sub_b_selected, sub_c_selected, sub_d_selected, sub_e_selected]
                if toUpdate not in schedule_data:
                    schedule_data.append(toUpdate)
                    show_tasks()
                    warning_label.set("")
                else:
                    warning_label.set("WARNING : task already added")



        elif main_selected == "any":
            warning_label.set("")

            process_any = True

            if sub_a_selected not in ["gainloss <=", "gainloss >=", "point >=", "diff >="]:
                warning_label.set("select box 2")
                process_any = False

            try:
                int(sub_b_selected)
            except:
                warning_label.set("box 3 is not a number")
                process_any = False

            if sub_c_selected not in ["alarm"]:
                warning_label.set("select box 4")
                process_any = False

            if sub_d_selected not in alarmTunes:
                warning_label.set("select box 5")
                process_any = False

            if process_any == True:

                toUpdate = [main_selected, sub_a_selected, sub_b_selected, sub_c_selected, sub_d_selected]
                if toUpdate not in schedule_data:
                    schedule_data.append(toUpdate)
                    show_tasks()
                    warning_label.set("")
                else:
                    warning_label.set("WARNING : task already added")


        elif main_selected == "error":
            warning_label.set("")

            process_error = True

            if sub_a_selected not in ["api", "sql", "main"]:
                warning_label.set("select box 2")
                process_error = False

            if sub_b_selected not in ["alarm"]:
                warning_label.set("select box 3")
                process_error = False

            if sub_c_selected not in alarmTunes:
                warning_label.set("select box 4")
                process_error = False

            if process_error == True:
                toUpdate = [main_selected, sub_a_selected, sub_b_selected, sub_c_selected]
                if toUpdate not in schedule_data:
                    schedule_data.append(toUpdate)
                    show_tasks()
                    warning_label.set("")
                else:
                    warning_label.set("WARNING : task already added")


        else:
            warning_label.set("select box 1")




        


    def main_condition():
        selected = main_combobox.get()
        if selected == "choose":
            pass

        if selected == "symbol":
            sub_a_combobox["values"] = all_symbols
            sub_a_combobox.set("choose")
            sub_b_combobox["values"] = ["ltp <=", "ltp >=", "point >=", "diff >="]
            sub_b_combobox.set("choose")
            sub_c_combobox["values"] = []
            sub_c_combobox.set("target")
            sub_d_combobox["values"] = ["buy", "sell", "alarm"]
            sub_d_combobox.set("choose")
            sub_e_combobox["values"] = []
            sub_e_combobox.set("choose")
            
        if selected == "order":
            sub_a_combobox["values"] = ordered_symbols
            sub_a_combobox.set("choose")
            sub_b_combobox["values"] = ["ltp <=", "ltp >=", "gainloss <=", "gainloss >=", "point >=", "diff >="]
            sub_b_combobox.set("choose")
            sub_c_combobox["values"] = []
            sub_c_combobox.set("target")
            sub_d_combobox["values"] = ["buy", "sell", "alarm"]
            sub_d_combobox.set("choose")
            sub_e_combobox["values"] = []
            sub_e_combobox.set("choose")

        if selected == "any":
            sub_a_combobox["values"] = ["gainloss <=", "gainloss >=", "point >=", "diff >="]
            sub_a_combobox.set("choose")
            sub_b_combobox["values"] = []
            sub_b_combobox.set("target")
            sub_c_combobox["values"] = ["alarm"]
            sub_c_combobox.set("choose")
            sub_d_combobox["values"] = []
            sub_d_combobox.set("choose")
            sub_e_combobox["values"] = []
            sub_e_combobox.set("choose")

        if selected == "error":
            sub_a_combobox["values"] = ["api", "sql", "main"]
            sub_a_combobox.set("choose")
            sub_b_combobox["values"] = ["alarm"]
            sub_b_combobox.set("choose")
            sub_c_combobox["values"] = []
            sub_c_combobox.set("choose")
            sub_d_combobox["values"] = []
            sub_d_combobox.set("choose")
            sub_e_combobox["values"] = []
            sub_e_combobox.set("choose")

    def sub_a_condition():
        selected = sub_a_combobox.get()

    def sub_b_condition():
        selected = sub_b_combobox.get()
        if selected == "choose":
            pass

        if selected == "alarm":
            sub_c_combobox["values"] = alarmTunes

    def sub_c_condition():
        selected = sub_c_combobox.get()
        if selected == "choose":
            pass

        if selected == "alarm":
            sub_d_combobox["values"] = alarmTunes

    def sub_d_condition():
        selected = sub_d_combobox.get()
        if selected == "choose":
            pass

        if selected == "alarm":
            sub_e_combobox["values"] = alarmTunes
            sub_e_combobox.set("choose")

        if selected == "buy" or selected == "sell":
            sub_e_combobox["values"] = []
            sub_e_combobox.set("quantity")

    def sub_e_condition():
        selected = sub_e_combobox.get()






    # main, sub_a, sub_b, sub_c, etc.

    all_symbols = list(tradeList.keys())
# >>>>>>>

    ordered_symbols = []

    for tradingsymbol in tradeList.keys():
        if orderQuantity[tradingsymbol] != 0:
            ordered_symbols.append(tradingsymbol)

# >>>>>>>
    alarmTunes = os.listdir("alerts/alarms")

    main_options = ["symbol", "order", "any", "error"]




    # datatype of menu text
    main_clicked = StringVar()

    main_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = main_clicked)
    main_combobox["values"] = main_options
    main_combobox.pack()
    main_combobox.bind("<<ComboboxSelected>>", lambda e: main_condition())
    main_combobox.place(x= 50, y= 50)
    main_combobox.set("choose")


    sub_a_clicked = StringVar()

    sub_a_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = sub_a_clicked)
    sub_a_combobox.pack()
    sub_a_combobox.bind("<<ComboboxSelected>>", lambda e: sub_a_condition())
    sub_a_combobox.place(x= 200, y= 50)
    sub_a_combobox.set("choose")


    sub_b_clicked = StringVar()

    sub_b_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = sub_b_clicked)
    sub_b_combobox.pack()
    sub_b_combobox.bind("<<ComboboxSelected>>", lambda e: sub_b_condition())
    sub_b_combobox.place(x= 350, y= 50)
    sub_b_combobox.set("choose")


    sub_c_clicked = StringVar()

    sub_c_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = sub_c_clicked)
    sub_c_combobox.pack()
    sub_c_combobox.bind("<<ComboboxSelected>>", lambda e: sub_c_condition())
    sub_c_combobox.place(x= 500, y= 50)
    sub_c_combobox.set("choose")


    sub_d_clicked = StringVar()

    sub_d_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = sub_d_clicked)
    sub_d_combobox.pack()
    sub_d_combobox.bind("<<ComboboxSelected>>", lambda e: sub_d_condition())
    sub_d_combobox.place(x= 650, y= 50)
    sub_d_combobox.set("choose")


    sub_e_clicked = StringVar()

    sub_e_combobox = ttk.Combobox(schedule_top, width = 10, textvariable = sub_e_clicked)
    sub_e_combobox.pack()
    sub_e_combobox.bind("<<ComboboxSelected>>", lambda e: sub_e_condition())
    sub_e_combobox.place(x= 800, y= 50)
    sub_e_combobox.set("choose")






# SCHEDULE WINDOW END






# section for functions

def convertINR(currencytofilter):
    return locale.currency(currencytofilter, grouping=True)
    
def changeColorToBlue(element):
    element.config(bg="blue", fg="white" )


def changeOnHover(button):

    button.bind("<Enter>", func=lambda e: hoverfunc())

    def hoverfunc():


        if button == tradingLabelButDict[0]:
            tabChange(0)

        elif button == tradingLabelButDict[1]:
            tabChange(1)
        elif button == tradingLabelButDict[2]:
            tabChange(2)
        elif button == tradingLabelButDict[3]:
            tabChange(3)
        elif button == tradingLabelButDict[4]:
            tabChange(4)
        elif button == tradingLabelButDict[5]:
            tabChange(5)
        elif button == tradingLabelButDict[6]:
            tabChange(6)
        elif button == tradingLabelButDict[7]:
            tabChange(7)
        elif button == tradingLabelButDict[8]:
            tabChange(8)
        elif button == tradingLabelButDict[9]:
            tabChange(9)
        elif button == tradingLabelButDict[10]:
            tabChange(10)
        elif button == tradingLabelButDict[11]:
            tabChange(11)
        elif button == tradingLabelButDict[12]:
            tabChange(12)
        elif button == tradingLabelButDict[13]:
            tabChange(13)
        elif button == tradingLabelButDict[14]:
            tabChange(14)
        elif button == tradingLabelButDict[15]:
            tabChange(15)
        elif button == tradingLabelButDict[16]:
            tabChange(16)
        elif button == tradingLabelButDict[17]:
            tabChange(17)

        else:
            print("button is not in range 0 - 17")

        changeColorToBlue(button)
        do_beep(1)



    button.bind("<Leave>", func=lambda e: button.config(
        bg="yellow", fg="black"))



# hover function for color codes


color_code_colors = ["white", "green", "yellow", "red", "blue"]
color_code_nav_dict = {}

def colorCodeHover(item, symbol):
    canvas.tag_bind(item, "<Enter>", func=lambda e: colorCodeHoverFunc())

    def colorCodeHoverFunc():
    

        # render color navigation
        nav_count = 0
        x = 1350
        y, r = 200, 20
        for color in color_code_colors:
            color_code_nav = "color_code_nav_"+str(nav_count)
            color_code_nav = canvas.create_oval( circle_coor(x, y, r, 1), circle_coor(x, y, r, 2), circle_coor(x, y, r, 3), circle_coor(x, y, r, 4), fill="white")
            color_code_nav_dict[nav_count] = color_code_nav

            # draw a round on the center circle
            if color == color_code_colors[2]:
                center_highlight_circle = canvas.create_oval( circle_coor(x, y, 25, 1), circle_coor(x, y, 25, 2), circle_coor(x, y, 25, 3), circle_coor(x, y, 25, 4), outline="black", width=3)
                color_code_nav_dict[5] = center_highlight_circle
            
            
            nav_count += 1
            x += 50



        # not dynamic if added more colors in color_code_colors list


        def nav_as_white():

            canvas.itemconfig(color_code_nav_dict[0], fill= "yellow")
            canvas.itemconfig(color_code_nav_dict[1], fill= "blue")
            canvas.itemconfig(color_code_nav_dict[2], fill= "white")
            canvas.itemconfig(color_code_nav_dict[3], fill= "green")
            canvas.itemconfig(color_code_nav_dict[4], fill= "red")

        def nav_as_green():

            canvas.itemconfig(color_code_nav_dict[0], fill= "blue")
            canvas.itemconfig(color_code_nav_dict[1], fill= "white")
            canvas.itemconfig(color_code_nav_dict[2], fill= "green")
            canvas.itemconfig(color_code_nav_dict[3], fill= "red")
            canvas.itemconfig(color_code_nav_dict[4], fill= "yellow")

        def nav_as_red():

            canvas.itemconfig(color_code_nav_dict[0], fill= "white")
            canvas.itemconfig(color_code_nav_dict[1], fill= "green")
            canvas.itemconfig(color_code_nav_dict[2], fill= "red")
            canvas.itemconfig(color_code_nav_dict[3], fill= "yellow")
            canvas.itemconfig(color_code_nav_dict[4], fill= "blue")

        def nav_as_yellow():

            canvas.itemconfig(color_code_nav_dict[0], fill= "green")
            canvas.itemconfig(color_code_nav_dict[1], fill= "red")
            canvas.itemconfig(color_code_nav_dict[2], fill= "yellow")
            canvas.itemconfig(color_code_nav_dict[3], fill= "blue")
            canvas.itemconfig(color_code_nav_dict[4], fill= "white")


        def nav_as_blue():

            canvas.itemconfig(color_code_nav_dict[0], fill= "red")
            canvas.itemconfig(color_code_nav_dict[1], fill= "yellow")
            canvas.itemconfig(color_code_nav_dict[2], fill= "blue")
            canvas.itemconfig(color_code_nav_dict[3], fill= "white")
            canvas.itemconfig(color_code_nav_dict[4], fill= "green")



        item_color = canvas.itemcget(item, "fill")

        if item_color == "white":
            nav_as_white()

        if item_color == "green":
            nav_as_green()

        if item_color == "red":
            nav_as_red()

        if item_color == "yellow":
            nav_as_yellow()

        if item_color == "blue":
            nav_as_blue()

        
        canvas.tag_bind(item, "<ButtonPress-1>", func=lambda e: colorCodeClickFunc())
        
        def colorCodeClickFunc():
            item_color = canvas.itemcget(item, "fill")

            if item_color == "white":
                canvas.itemconfig(item, fill= "green")
                nav_as_green()

            if item_color == "green":
                canvas.itemconfig(item, fill= "red")
                nav_as_red()

            if item_color == "red":
                canvas.itemconfig(item, fill= "yellow")
                nav_as_yellow()

            if item_color == "yellow":
                canvas.itemconfig(item, fill= "blue")
                nav_as_blue()

            if item_color == "blue":
                canvas.itemconfig(item, fill= "white")
                nav_as_white()

            db.updb_colornote(symbol, canvas.itemcget(item, "fill"))


    canvas.tag_bind(item, "<Leave>", func= lambda e: delete_color_code_nav())

    def delete_color_code_nav():
        nav_count = 0
        for color in color_code_colors:
            canvas.delete(color_code_nav_dict[nav_count])
            nav_count += 1

        # delete round on the center circle
        canvas.delete(color_code_nav_dict[5])



# function to update tkinter with data and history using multiple threads



def data_thread(trading_symbol, value1, value2, value3, value4, value5):
    stockList.item(trading_symbol, text='', values=(value1, value2, value3, value4, value5))


def his_thread(trading_symbol, value1):
    stockList.item(trading_symbol, text='', values=(value1, "", "", "", ""))

global gainLossButtonNameDict
gainLossButtonNameDict= {}

def gainLoss_thread(symbol):
    global gainLossButtonNameDict

    if symbol in gainLossButtonNameDict:
        gainLossButtonNameDict[symbol].configure(text= whatGainLoss(symbol))

        # loss or gain color
        gainorloss = int(gainLossButtonNameDict[symbol]['text'])
        if gainorloss < 0:
            gainLossButtonNameDict[symbol].configure(bg= "#ff6600")
        
        if gainorloss > 0:
            gainLossButtonNameDict[symbol].configure(bg= "#39e75f")



# function to find iid of tkinter treeview

def findiid(tradingsymbol, data_his):

    if data_his == 0:
        iidout = tradingdata_count_dict[tradingsymbol]

    if data_his == 1:
        iidout = tradingdatahis_count_dict[tradingsymbol]

    return iidout
    


# function to update tkinter gui point row color in ascending order
global updated_odd
updated_odd = []

def tkinter_point_row(points_data):
    global updated_odd
    for iid in updated_odd:
        stockList.item(iid, tags= "oddrow")
        updated_odd = []

    # red row start(1)

    RED_TARGET = 0.25

    collected_iid = []
    collected_symbols = []
    for key, value in points_data.items():
        if value >= RED_TARGET:
            collected_iid.append(findiid(key, 0))
            collected_symbols.append(key)
        
    # red row end(1)

    # change red colornote to blue if any red row occurs start

    for symbol in collected_symbols:
        item_color = canvas.itemcget(colorCodeDict[symbol], "fill")
        if item_color == "red":
            canvas.itemconfig(colorCodeDict[symbol], fill= "blue")


    # change red colornote to blue if any red row occurs end

    sorted_points_data = sorted(points_data.items(), key=lambda x:x[1]) # key=lambda x:x[1] means to sort value of dict.
    

    aiid = findiid(sorted_points_data[-1][0], 0)
    biid = findiid(sorted_points_data[-2][0], 0)
    ciid = findiid(sorted_points_data[-3][0], 0)


    # change red colornote to blue if any pink row occurs start

    def item_red_to_blue(symbol, color):

        if color == "red":
            canvas.itemconfig(colorCodeDict[symbol], fill= "blue")


    item_color1 = canvas.itemcget(colorCodeDict[ sorted_points_data[-1][0] ], "fill")
    item_red_to_blue( sorted_points_data[-1][0], item_color1)
    item_color2 = canvas.itemcget(colorCodeDict[ sorted_points_data[-2][0] ], "fill")
    item_red_to_blue( sorted_points_data[-2][0], item_color2)
    item_color3 = canvas.itemcget(colorCodeDict[ sorted_points_data[-3][0] ], "fill")
    item_red_to_blue( sorted_points_data[-3][0], item_color3)

    # change red colornote to blue if any pink row occurs end


    stockList.item(aiid, tags= "ahigh_point_row")
    stockList.item(biid, tags= "bhigh_point_row")
    stockList.item(ciid, tags= "chigh_point_row")


    stockList.tag_configure('ahigh_point_row', background='#ff4284', foreground='black') # dark pink
    stockList.tag_configure('bhigh_point_row', background='#fa5da2', foreground='black') # light pink
    stockList.tag_configure('chigh_point_row', background='#f584d2', foreground='black') # v light pink
    

    updated_odd = [aiid, biid, ciid]
    

    # red row start(2)
    for id in collected_iid:

        stockList.item(id, tags= "targeted_red_row")
        stockList.tag_configure('targeted_red_row', background='red', foreground='white') # red row

        updated_odd.append(id)

    # red row end(2)




# function to make beep sound

def do_beep(beep):

    def make_beep_sound():
        playsound('alerts/beeps/beep-'+str(beep)+'.mp3')

    thread_of_beep = threading.Thread(target=make_beep_sound)
    thread_of_beep.start()







# section for tkinter


# Create an instance of Style widget
style=ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Headings", font=(None, 10))
style.configure('Treeview', rowheight=25)

# variables

tradingsymbolButSuffix = "_switch"
switchCount = 0
tradingsymbolButY = 40
tradingLabelButDict = {}


colorCodeY = 55
colorCodeDict = {}



#table of stocks
stock_frame = Frame(win)
stock_frame.pack()
stock_frame.place(x=0,y=0)

global stockList
stockList = ttk.Treeview(stock_frame, height = 36)

stockList['columns'] = ('column1', 'column2', 'column3', 'column4','column5')

stockList.column("#0", width=0, stretch=NO)
stockList.column("column1",anchor=CENTER, width=280)
stockList.column("column2",anchor=CENTER, width=100)
stockList.column("column3",anchor=CENTER, width=100)
stockList.column("column4",anchor=CENTER, width=100)
stockList.column("column5",anchor=CENTER, width=100)



stockList.heading("#0",text="",anchor=CENTER)
stockList.heading("column1",text="TRADE",anchor=CENTER)
stockList.heading("column2",text="LTP-C",anchor=CENTER)
stockList.heading("column3",text="LTP-D",anchor=CENTER)
stockList.heading("column4",text="LTP-P",anchor=CENTER)
stockList.heading("column5",text="PUT (100)",anchor=CENTER)

iidcountodd = 0
iidcounteven = 1
tradingdata_count_dict = {}
tradingdatahis_count_dict = {}


for tradingsymbol in tradeList.keys():

    # render trading data
    stockList.insert(parent='', index='end', iid=iidcountodd, text='', tags = ('oddrow'), values=("", "", "", "", ""))
    stockList.tag_configure('oddrow', background='orange', foreground='black')

    tradingdata_count_dict[tradingsymbol] = iidcountodd
    iidcountodd += 2

    # render ltp diff history
    stockList.insert(parent='', index='end', iid=iidcounteven, text='', tags = ('evenrow'), values=("", "", "", "", ""))
    stockList.tag_configure('evenrow', background='purple', foreground='white')

    tradingdatahis_count_dict[tradingsymbol] = iidcounteven
    iidcounteven += 2

    stockList.pack()





    # render remote browser tab switch buttons

    switchButton = tradingsymbol+tradingsymbolButSuffix
    switchButton = tk.Button(text="SWITCH", bg= "yellow")
    switchButton.pack()
    switchButton.place(x= 700, y= tradingsymbolButY)
    tradingsymbolButY += 50
    tradingLabelButDict[switchCount] = switchButton
    switchCount += 1

    changeOnHover(switchButton)



    # render color codes

    def circle_coor(x, y, r, pos):

        if pos == 1:
            return x-r
        if pos == 2:
            return y-r
        if pos == 3:
            return x+r
        if pos == 4:
            return y+r



    x, r = 765, 8
    color_code = canvas.create_oval( circle_coor(x, colorCodeY, r, 1), circle_coor(x, colorCodeY, r, 2), circle_coor(x, colorCodeY, r, 3), circle_coor(x, colorCodeY, r, 4), fill="white")
    colorCodeY += 50
    colorCodeDict[tradingsymbol] = color_code


    colorCodeHover(color_code, tradingsymbol)







    # render remote browser tab switch to < profile >

    profile_switchButton = tk.Button(text="VIEW PROFILE", bg= "#7A2048", fg="white")
    profile_switchButton.pack()
    profile_switchButton.place(x= 1340, y= 350)
    profile_switchButton.bind("<Enter>", func=lambda e: profile_switchButton_config(profile_switchButton))

    def profile_switchButton_config(button):
        tabChange(18)
        changeColorToBlue(button)

        button.bind("<Leave>", func=lambda e: button.config(bg="#7A2048", fg="white"))


    # render exit button
    exit_button = tk.Button(text= "EXIT", bg= "#7A2048", fg="white", command= lambda: exit_button_function())
    exit_button.pack()
    exit_button.place(x= 1460, y= 350)
    exit_button.bind("<Enter>", func=lambda e: changeColorToBlue(exit_button))
    exit_button.bind("<Leave>", func=lambda e: exit_button.config(bg="#7A2048", fg="white"))

    def exit_button_function():
        db.close_db()
        exit()



    # render scheduler button

    
    scheduler_button = tk.Button(text= "SCHEDULE", bg= "#7A2048", fg="white", command= lambda: open_schedule_win())
    scheduler_button.pack()
    scheduler_button.place(x= 1515, y= 350)
    scheduler_button.bind("<Enter>", func=lambda e: changeColorToBlue(scheduler_button))
    scheduler_button.bind("<Leave>", func=lambda e: scheduler_button.config(bg="#7A2048", fg="white"))






# thread section for api (stock data)


def thread_api_stock_data():
    try:
        totp = pyotp.TOTP(configs.totp).now()
        global obj
        obj=SmartConnect(api_key=configs.api_key)
        data = obj.generateSession(configs.user_id,configs.password,totp)

        refreshToken= data['data']['refreshToken']



        feedToken=obj.getfeedToken()
    except Exception as e:
        print("\n\n\n\n\nError while connecting to api\n\n\n\n\n")
        print(e)
        sleep(0.5)
        win.configure(background='red')

    #start making variables


    exchange = "NSE"

    LTP_History = {}

    global LTP_Stored
    LTP_Stored = {}

    for tradingsymbol, symboltoken in tradeList.items():
        
        LTP_History[tradingsymbol] = []
        
        LTP_Stored[tradingsymbol] = 0.0

    while True:

        try:
            
            win.configure(background='green')

            # merge tradingdata
            trading_data_merge_prefix = "merged_"
            trading_data_merged = {}
            trading_data_his_merged = {}
            
            points_data_rec = {}

            for tradingsymbol, symboltoken in tradeList.items():
                


                #start populating data

                #update LTP-C

                LTP = obj.ltpData(exchange, tradingsymbol, symboltoken)
                ltp = LTP["data"]["ltp"]


                #update LTP-D
                if LTP_Stored[tradingsymbol] != 0:
                    diff = ltp-LTP_Stored[tradingsymbol]
                else:
                    diff = 0

                #store history of diff
                if (len(LTP_History[tradingsymbol]) > 7):
                    LTP_History[tradingsymbol].pop(0)

                LTP_History[tradingsymbol].append(round(diff, 3))


                LTP_Stored[tradingsymbol] = ltp

                #update LTP-P

                diff_whole_data = LTP_History[tradingsymbol][-1] - LTP_History[tradingsymbol][0]


                if (diff_whole_data==0):
                    point = 0

                else:
                    point = abs( round( (diff_whole_data/ltp)*100, 3 ) )


                #calculate amount needed for 100 stock
                put = round((ltp*100)/5)



                trading_data_merge_key = trading_data_merge_prefix + tradingsymbol
                trading_data_merged[trading_data_merge_key] = [tradingsymbol, ltp, round(diff, 3), point, convertINR(put)]
                trading_data_his_merged[trading_data_merge_key] = LTP_History[tradingsymbol]

                points_data_rec[tradingsymbol] = point

            # update tkinter GUI with data
            for tradingsymbol in tradeList.keys():
                trading_data_merge_key = trading_data_merge_prefix + tradingsymbol

            # >>> data
                thread_data = threading.Thread(target=data_thread(tradingdata_count_dict[tradingsymbol], trading_data_merged[trading_data_merge_key][0], trading_data_merged[trading_data_merge_key][1], trading_data_merged[trading_data_merge_key][2], trading_data_merged[trading_data_merge_key][3], trading_data_merged[trading_data_merge_key][4]))
                thread_data.start()

                
            # >>> history
                thread_his = threading.Thread(target=his_thread(tradingdatahis_count_dict[tradingsymbol], trading_data_his_merged[trading_data_merge_key] ))
                thread_his.start()


            # >>> whatGainLoss
                thread_gainLoss = threading.Thread(target=gainLoss_thread(tradingsymbol))
                thread_gainLoss.start()
                

            # update gui with point color in ascending order
            tkinter_point_row(points_data_rec)


            sleep(0)
        except Exception as e:
            win.configure(background='red')
            print (e)
            sleep(0.5)
            print("exception - retrying")








# thread section for api (trading)

def thread_api_trade():

    # configs of the tradingsymbol

    #  >>> stored order data
    global orderDataStored, orderQuantity
    orderDataStored = {}
    orderQuantity = {}

    for tradingsymbol in tradeList.keys():
        # this dict will be filled by updateOrderData()
        orderDataStored[tradingsymbol] = []
        orderQuantity[tradingsymbol] = 0






    #functions



    def stockQuaRelease(symbol):
        stockQuantity = stockQuaButDict[symbol]['text']
        stockQuantity = int(abs(stockQuantity))
        if stockQuantity == 0:
            return None


        if stockQuantity < 0:
            #buy it
            



            orderparams = {
                
                "variety":"NORMAL",
                "tradingsymbol":symbol,
                "symboltoken":tradeList[symbol],
                "transactiontype":"BUY",
                "exchange":"NSE",
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                # "price":"194.50",  The min or max price to execute the order at (for LIMIT orders)
                # "squareoff":"0",   Only For ROBO (Bracket Order)
                # "stoploss":"0",    Only For ROBO (Bracket Order)
                "quantity":stockQuantity

            }

            try:
                if configs.test_mode != 1:
                    orderID = obj.placeOrder(orderparams)
                    log_section.insert(END, f"{rule} {symbol} {str(stockQuantity)} ID: {orderID}\n")
                fundsmargins()

            except:
                log_section.insert(END, f"error while executing : {rule} {symbol} {str(stockQuantity)}\n")
                fundsmargins()

                # update db log table
                try:
                    db.updb_log(log_section.get(1.0, "end-1c"))
                except:
                    print("error while updating log db - retrying")
                    db.updb_log(log_section.get(1.0, "end-1c"))
                
                return None






            if symbol in gainLossButtonNameDict.keys():
                deleteElement_DictKey(symbol)


        if stockQuantity > 0:


            orderparams = {
                
                "variety":"NORMAL",
                "tradingsymbol":symbol,
                "symboltoken":tradeList[symbol],
                "transactiontype":"SELL",
                "exchange":"NSE",
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                # "price":"194.50",  The min or max price to execute the order at (for LIMIT orders)
                # "squareoff":"0",   Only For ROBO (Bracket Order)
                # "stoploss":"0",    Only For ROBO (Bracket Order)
                "quantity":stockQuantity

            }
            
            try:
                if configs.test_mode != 1:
                    orderID = obj.placeOrder(orderparams)
                    log_section.insert(END, f"{rule} {symbol} {str(stockQuantity)} ID: {orderID}\n")
                fundsmargins()

            except:
                log_section.insert(END, f"error while executing : {rule} {symbol} {str(stockQuantity)}\n")
                fundsmargins()

                # update db log table
                try:
                    db.updb_log(log_section.get(1.0, "end-1c"))
                except:
                    print("error while updating log db - retrying")
                    db.updb_log(log_section.get(1.0, "end-1c"))
                
                return None
            
        
        



            if symbol in gainLossButtonNameDict.keys():
                deleteElement_DictKey(symbol)




        

        # delete orderdata from db


        try:
            db.delete_orderdata(symbol)
        except:
            print(f"error while deleting orderdata of symbol {symbol} - retrying")
            db.delete_orderdata(symbol)
        
        # update db log table


        try:
            db.updb_log(log_section.get(1.0, "end-1c"))
        except:
            print("error while updating log db - retrying")
            db.updb_log(log_section.get(1.0, "end-1c"))



        stockQuaButDict[symbol].configure(text = 0)
        stockQuaButDict[symbol].configure(bg= "yellow")



        


    # to update the orderDataStored dictionary
        

    def updateOrderData(symbol, quantity, buysell):
        quantity = int(quantity)
        totalAmount = (LTP_Stored[symbol] * quantity)/5


        orderDataStored[symbol] = orderDataStored[symbol] + [totalAmount, buysell]


        if buysell == "buy":
            orderQuantity[symbol] = orderQuantity[symbol] + quantity
        else:
            orderQuantity[symbol] = orderQuantity[symbol] - quantity




    # to calculate realtime gain loss

    global whatGainLoss
    def whatGainLoss(symbol):
        currentAmount = (LTP_Stored[symbol] * orderQuantity[symbol])/5
        if orderDataStored[symbol] != []:

            amountList = (orderDataStored[symbol][::2])
            buySellList = [value for value in orderDataStored[symbol] if value not in orderDataStored[symbol][::2]]

            whatGainLossOut = 0
            counter = 0
            for data in buySellList:
                if data == "buy":
                    whatGainLossOut = (whatGainLossOut - amountList[counter])


                if data == "sell":
                    whatGainLossOut = (amountList[counter] + whatGainLossOut)

                counter += 1

            whatGainLossOut = round(whatGainLossOut + currentAmount, 3)

            return whatGainLossOut
            


    def deleteElement_DictKey(symbol):
        
        gainLossButtonNameDict[symbol].destroy()
        gainLossButtonNameDict.pop(symbol)
    


    #to execute order
    global gainLossButtonNameDict
    gainLossButtonNameDict = {}

    global stockExec
    def stockExec(symbol, quantity, exec, customrule):
        global rule
        quantity = int(quantity)
        if quantity == 0:
            return None

        positionY= stockQuanYDict[symbol]-5


        if customrule == "buy":
            rule = "buy"
        if customrule == "sell":
            rule = "sell"




        #>>>>>> execute order here { only if exec == 1 }
        if exec == 1:


            orderparams = {
                
                "variety":"NORMAL",
                "tradingsymbol":symbol,
                "symboltoken":tradeList[symbol],
                "transactiontype":rule.upper(),
                "exchange":"NSE",
                "ordertype":"MARKET",
                "producttype":"INTRADAY",
                "duration":"DAY",
                # "price":"194.50",  The min or max price to execute the order at (for LIMIT orders)
                # "squareoff":"0",   Only For ROBO (Bracket Order)
                # "stoploss":"0",    Only For ROBO (Bracket Order)
                "quantity":quantity

            }

            try:
                if configs.test_mode != 1:
                    orderID = obj.placeOrder(orderparams)
                    log_section.insert(END, f"{rule} {symbol} {str(quantity)} ID: {orderID}\n")
                fundsmargins()

            except:
                log_section.insert(END, f"error while executing : {rule} {symbol} {str(quantity)}\n")
                fundsmargins()

                # update db log table
                try:
                    db.updb_log(log_section.get(1.0, "end-1c"))
                except:
                    print("error while updating log db - retrying")
                    db.updb_log(log_section.get(1.0, "end-1c"))
                
                return None



            






        # update db log table
        try:
            db.updb_log(log_section.get(1.0, "end-1c"))
        except:
            print("error while updating log db - retrying")
            db.updb_log(log_section.get(1.0, "end-1c"))
            
        

        

        # pack gain or loss GUI
        gainLossButtonPrefix = "gain_loss_"

        gainLossButtonName = gainLossButtonPrefix+symbol
        updateOrderData(symbol, quantity, rule)

        if symbol not in gainLossButtonNameDict.keys():

            
            gainLossButtonName = tk.Button(win, background= "yellow", foreground= "black", text= whatGainLoss(symbol), height= 1, command= lambda : deleteElement_DictKey(symbol))
            gainLossButtonName.pack()
            gainLossButtonName.place(x= 1250, y= positionY)

            gainLossButtonNameDict[symbol] = gainLossButtonName



        # else:
        #     gainLossButtonName.configure(text=whatGainLoss(symbol))




        #update stock quantity
        stockQuantity = stockQuaButDict[symbol]['text']
        overallStatus = ""

        if rule == "buy":
            stockQuantity += quantity
            stockQuaButDict[symbol].configure(text = stockQuantity)

        if rule == "sell":
            stockQuantity -= quantity
            stockQuaButDict[symbol].configure(text = stockQuantity)



        if stockQuantity < 0:
            stockQuaButDict[symbol].configure(bg= "#ff6600")
            overallStatus = "sell"
        
        elif stockQuantity > 0:
            stockQuaButDict[symbol].configure(bg= "#39e75f")
            overallStatus = "buy"
        else:
            stockQuaButDict[symbol].configure(bg= "yellow")
            deleteElement_DictKey(symbol)

        # >>>>>> update db with orderdata
        if int(abs(stockQuantity)) == 0:
            try:
                db.delete_orderdata(symbol)
            except:
                print(f"error while deleting orderdata of symbol {symbol} - retrying")
                db.delete_orderdata(symbol)

        else:
            
            try:
                db.updb_orderdata(symbol, abs(stockQuantity), overallStatus)
            except:
                print(f"error while updating orderdata db of {symbol} - retrying")
                db.updb_orderdata(symbol, abs(stockQuantity), overallStatus)



    global fundsmargins
    def fundsmargins():
        global obj
        try:
            rms = obj.rmsLimit()
            rms_net = rms['data']['net']
            rms_availablecash = rms['data']['availablecash']
            rms_availableintradaypayin = rms['data']['availableintradaypayin']
            rms_availablelimitmargin = rms['data']['availablelimitmargin']
            
            fundsmargins_section.delete("1.0", "end")
            fundsmargins_section.insert(END, f"net : {rms_net}\navailable cash : {rms_availablecash}\navailable intra pay in : {rms_availableintradaypayin}\navailable limit margin : {rms_availablelimitmargin}\n")
        except:
            fundsmargins_section.insert(END,"Error while retrieving funds and margins RMS")




    #to listen to mouse < left and right > click

    # change button color, swap buy or sell (right click)

    global buttonBack, rule
    rule = "buy"
    buttonBack = "green"
    buttonFor = "white"


    def on_right_click(event):
        global buttonBack, rule

        if buttonBack == "green":
            rule = "sell"
            for i in stockButtonNameList:
                i.configure(bg = "red")
            buttonBack = "red"

        elif buttonBack == "red":
            rule = "buy"
            for i in stockButtonNameList:
                i.configure(bg = "green")
            buttonBack = "green"

    # clear tkinter treeview selection (left click)
    def on_left_click(event):

        if len(stockList.selection()) > 0:
            stockList.selection_remove(stockList.selection()[0])




    canvas.bind("<Button-1>", on_left_click) #Button-1 is mouse left click
    canvas.bind("<Button-3>", on_right_click) #Button-3 is mouse right click
    
    canvas.pack()
    canvas.focus_set()





    #render area starts

    tradingbuttonX = 800
    tradingsymbolY = 44
    stockQuantity = [5,10,30,50,100,200,300,400,500]

    stockButtonVarPrefix = "stockButton"  #to make the button name unique
    stockButtonVarSuffix = 0
    stockButtonNameList = []

    stockQuaPlacedSuffix = "_quan"  #to make the button name unique
    stockQuaButDict = {}
    stockQuanYDict = {}

    for tradingsymbol in tradeList.keys():

        #render trading symbol
        # a = {tradingsymbol: tk.Label(text=tradingsymbol).place(x=1000, y=tradingsymbolY)}
        
        # store stock quantity buttons y axis in this dict
        
        stockQuanYDict[tradingsymbol] = tradingsymbolY
        for stock in stockQuantity:
            
            #render stock quantity buttons
            stockButtonName = stockButtonVarPrefix+str(stockButtonVarSuffix)
            stockButtonName = tk.Button(win, background= buttonBack, foreground= buttonFor, text= stock, height= 1, command= lambda symbol= tradingsymbol, stock= stock, positionY = tradingsymbolY-5: stockExec(symbol, stock, 1, ""))
            stockButtonName.pack()
            stockButtonName.place(x= tradingbuttonX, y= tradingsymbolY-5)

            tradingbuttonX += 40
            stockButtonNameList.append(stockButtonName)
            stockButtonVarSuffix += 1

            stockButtonName.bind("<Enter>", func=lambda e:do_beep(3))

        #render stock quantity placed button
        stockQuaButName = tradingsymbol+stockQuaPlacedSuffix
        stockQuaButName = tk.Button(win, background= "yellow", foreground= "black", text= 0, height= 1, command= lambda symbol= tradingsymbol: stockQuaRelease(symbol))
        stockQuaButName.pack()
        stockQuaButName.place(x= tradingbuttonX + 30, y= tradingsymbolY-5)
        stockQuaButDict[tradingsymbol] = stockQuaButName


        tradingsymbolY += 50
        tradingbuttonX = 800



    #Text Area for log section
    global log_section
    log_section = tk.Text(background="#001755", foreground="white", width= 40, height=25)
    log_section.pack()
    log_section.place(x=1340,y=400)



    #Text Area for funds and margins
    global fundsmargins_section
    fundsmargins_section = tk.Text(background="#001755", foreground="white", width= 40, height=5)
    fundsmargins_section.pack()
    fundsmargins_section.place(x=1340, y=232)

    fundsmargins()

    fundsmargins_section.bind("<Enter>", func=lambda e:fundsmargins())




    win.mainloop()





def thread_check_schedule():
    pass




# start api threads
thread_stock_api = threading.Thread(target = thread_api_stock_data)
thread_stock_api.start()

thread_trade_api = threading.Thread(target = thread_api_trade)
thread_trade_api.start()

# start schedule thread
thread_schedule_check = threading.Thread(target = thread_check_schedule)
thread_schedule_check.start()



win.mainloop()
