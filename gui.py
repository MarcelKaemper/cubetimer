import time
import serial
import serial.tools.list_ports
import tkinter
import threading


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
            txt.insert(0, (str(round(timeend-timest, 4))))

    s.close()


root = tkinter.Tk()
root.title("Cubetimer - GUI")

frame = tkinter.Frame()
frame.pack()

txt = tkinter.Entry(frame, bd=5, insertwidth=1, font=30)
txt.pack()


t = threading.Thread(target=timer, daemon=True)
t.start()
root.mainloop()
