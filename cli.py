import time
import serial
import serial.tools.list_ports
import functions as core

ports = core.loadPorts() 
for i in range(len(ports)):
    print("["+str(i+1)+"] "+ports[i])

s = serial.Serial(ports[int(input())-1])

timest = ""
timeend = ""

while 1:
    try:
        serial = s.readline().decode("utf-8").replace("\n","")
        print(serial)
        if serial == "tmr_start\r":
            timest = time.time()
        elif serial == "tmr_stop\r":
            timeend = time.time()

        if timest != "" and timeend != "":
            print("Time needed: ", round(timeend - timest, 4), " secs")
            timest = ""
            timeend = ""
        
    except KeyboardInterrupt:
        break


s.close()
