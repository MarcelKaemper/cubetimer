import time
import serial
import serial.tools.list_ports
import tkinter
import threading

def saveTime(timeCurr):
    with open("times.data", "a") as w:
        w.write(timeCurr+"\n")

def loadTimes():
    cbb.delete(0, tkinter.END)
    for item in readTimes():
        cbb.insert(tkinter.END, item)


def readTimes():
    times = []
    with open("times.data", "r") as r:
        for line in r.readlines():
            times.append(line)
    return times

def deleteItem():
    try:
        toDelete = cbb.get(cbb.curselection())
        print(cbb.get(cbb.curselection()))
        with open("times.data", "r") as f:
            lines = f.readlines()
        with open("times.data", "w") as f:
            for line in lines:
                if line != toDelete:
                    f.write(line)
        loadTimes()
    except:
        pass


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


#####################
### Layout
#####################

root = tkinter.Tk()
root.geometry("500x500")
root.title("Cubetimer - GUI")

frame = tkinter.Frame()
frame.pack()

txt = tkinter.Entry(frame, bd=5, insertwidth=1, font=30)
txt.pack()

dele = tkinter.Button(frame, text="delete", command=deleteItem)
dele.pack()

cbb = tkinter.Listbox(frame) 
loadTimes()
cbb.pack()


t = threading.Thread(target=timer, daemon=True)
t.start()

root.mainloop()
