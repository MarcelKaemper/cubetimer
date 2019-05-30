import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

s = serial.Serial("COM9")

while 1:
    try:
        serial = s.readline().decode("utf-8").replace("\n","")
        print(serial)
    except KeyboardInterrupt:
        break

s.close()
