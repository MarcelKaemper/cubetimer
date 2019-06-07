import serial.tools.list_ports
import random

def loadPorts():
    ports = [] 
    for p in serial.tools.list_ports.comports():
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

    return scr

def readTimes():
    times = []
    with open("times.data", "r") as r:
        for line in r.readlines():
            times.append(line)
    return times

def saveTime(timeCurr):
    with open("times.data", "a") as w:
        w.write(timeCurr+"\n")