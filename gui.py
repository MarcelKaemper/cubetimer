import time
import serial
import tkinter
import threading
import tkinter.ttk as ttk
import functions as core

def refreshAll():
    loadTimes()
    scrambleTxt["text"] = core.scramble()

def getAvg(n):
    sum = 0
    for i in range(0,n):
        try:
            sum+=float(cbb.get(i).replace("\n", ""))
        except Exception:
            return 0
            
    return round(sum/n,4)

def loadTimes():
    cbb.delete(0, tkinter.END)
    for item in core.readTimes():
        cbb.insert(0, item)
    avg_three["text"] = "Avg. 3: "+str(getAvg(3))
    avg_five["text"] = "Avg. 5: "+str(getAvg(5))
    avg_twelve["text"] = "Avg. 12: "+str(getAvg(12))
    avg_thirty["text"] = "Avg. 30: "+str(getAvg(30))
    scrambleTxt["text"] = core.scramble()

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

            core.saveTime(timeCurr)
            
            cbb.insert(0, timeCurr)
            # loadTimes()

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
ports = core.loadPorts()
port["values"] = ports
port.current(0)

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
