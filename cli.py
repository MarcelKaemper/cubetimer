import time
import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

s = serial.Serial("COM9")

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
            break
        
    except KeyboardInterrupt:
        break

print("Time needed: ", round(timeend - timest, 4), " secs")

s.close()
