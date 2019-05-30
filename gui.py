import time
import serial
import serial.tools.list_ports
import tkinter
import threading
from tkinter import ttk

def saveTime(timeCurr):
    with open("times.data", "a") as w:
        w.write(timeCurr+"\n")


def readTime():
    times = []
    with open("times.data", "r") as r:
        for line in r.readlines():
            times.append(line)
    return times


def timer():
    s = serial.Serial("COM9")

    timest = ""
    timeend = ""

    while 1:
        ser = s.readline().decode("utf-8").replace("\n","")
        print(ser)

        if ser == "tmr_start\r":
            timest = time.time()
        elif ser == "tmr_stop\r":
            timeend = time.time()

        if timest != "" and timeend != "":
            timeCurr = str(round(timeend-timest,4))

            txt.delete(0, tkinter.END)
            txt.insert(0, timeCurr)

            saveTime(timeCurr)

            timeCurr = ""
            timest = ""
            timeend = ""

    s.close()



root = tkinter.Tk()
root.geometry("500x500")
root.title("Cubetimer - GUI")

frame = tkinter.Frame()
frame.pack()

txt = tkinter.Entry(frame, bd=5, insertwidth=1, font=30)
txt.pack()

var = ""

cbb = tkinter.Listbox(frame) 
for item in readTime():
    cbb.insert(tkinter.END, item)
cbb.pack()


t = threading.Thread(target=timer, daemon=True)
t.start()
root.mainloop()
