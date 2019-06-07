import time
import serial
import serial.tools.list_ports
import tkinter
import threading
import tkinter.ttk as ttk
import random

def refreshAll():
    ports = loadPorts()
    loadTimes()
    scramble()
    port["values"] = ports
    port.current(0)
        


def loadPorts():
    ports = [] 
    for p in serial.tools.list_ports.comports():
        print(p[0])
        ports.append(p[0])
    return ports

def scramble():
    x = ["R", "L", "U", "D", "F", "B"]
    y = [" ", " ", " ", "'", "2"]

    scr = ""

    prev = ""

    for i in range(0,12):
        while 1:
            pick = random.choice(x)
            if pick != prev:
                break

        prev = pick
        addition = random.choice(y)
        if addition=="2":
            temp = pick
            pick = addition
            pick += temp
        else:
            pick += addition
        scr += pick+" "
        pick = ""

    scrambleTxt["text"] = scr

def getAvg(n):
    sum = 0
    for i in range(0,n):
        try:
            sum+=float(cbb.get(i).replace("\n", ""))
        except Exception:
            return 0
            
    return round(sum/n,4)


def saveTime(timeCurr):
    with open("times.data", "a") as w:
        w.write(timeCurr+"\n")

def loadTimes():
    cbb.delete(0, tkinter.END)
    for item in readTimes():
        cbb.insert(0, item)
    avg_three["text"] = "Avg. 3: "+str(getAvg(3))
    avg_five["text"] = "Avg. 5: "+str(getAvg(5))
    avg_twelve["text"] = "Avg. 12: "+str(getAvg(12))
    avg_thirty["text"] = "Avg. 30: "+str(getAvg(30))
    scramble()


def readTimes():
    times = []
    with open("times.data", "r") as r:
        for line in r.readlines():
            times.append(line)
    return times

def deleteItem():
    try:
        toDelete = cbb.get(cbb.curselection())
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
    s = serial.Serial(port.get())
    tmpFrame.destroy()

    timest = ""
    timeend = ""

    while 1:
        ser = s.readline().decode("utf-8").replace("\n","")

        if ser == "tmr_start\r":
            timest = time.time()
            txt.insert(tkinter.END, "Running!")
        elif ser == "tmr_stop\r":
            timeend = time.time()

        if timest != "" and timeend != "":
            timeCurr = str(round(timeend-timest,4))

            txt.delete(0, tkinter.END)
            txt.insert(0, timeCurr)

            saveTime(timeCurr)
            loadTimes()

            timeCurr = ""
            timest = ""
            timeend = ""

    s.close()

def go():
    t = threading.Thread(target=timer, daemon=True)
    t.start()


#####################
### Layout
#####################

root = tkinter.Tk()
# root.geometry("500x500")

root.title("Cubetimer - GUI")

tmpFrame = tkinter.Frame()
tmpFrame.pack(side=tkinter.TOP)

frame = tkinter.Frame()
frame.pack()

btnFrame = tkinter.Frame()
btnFrame.pack(side=tkinter.TOP)

port = ttk.Combobox(tmpFrame)
port.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
startBtn = tkinter.Button(tmpFrame, text="Choose", command=go)
startBtn.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

txt = tkinter.Entry(frame, bd=5, insertwidth=1, font=30)
txt.pack()

scrambleTxt = tkinter.Label(frame)
scrambleTxt.pack()

avg_three = tkinter.Label(frame)
avg_three.pack()

avg_five = tkinter.Label(frame)
avg_five.pack()

avg_twelve = tkinter.Label(frame)
avg_twelve.pack()

avg_thirty = tkinter.Label(frame)
avg_thirty.pack()

refresh = tkinter.Button(btnFrame, text="Refresh", command=refreshAll)
refresh.pack(side=tkinter.LEFT)
dele = tkinter.Button(btnFrame, text="Delete", command=deleteItem)
dele.pack(side=tkinter.LEFT)

cbb = tkinter.Listbox(frame) 
cbb.pack()

refreshAll()

root.mainloop()
