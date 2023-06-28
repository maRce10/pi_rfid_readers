import time
import serial
from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

Tag1=str('')
Tag2 = str ('')

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.output(23, False)
GPIO.output(24, False)

PortFP = serial.Serial('/dev/ttyAMAO', 9600)

while True:
    ID = ''
    read_byte = PortRF.read().decode("utf-8")
    if read_byte == "\x02":
        for Counter in range(12):
            read_byte = PortRF.read()
            ID = ID + str(read_byte)
            #print(hex(ord(read_byte)))
        ID = ID.replace("b","").replace("'","")
        print(ID)
        now = datetime.now()
        if ID == Tag1:
            print("matched 1:  ", now)
            GPIO.output(23, True)
            GPIO.output(24, False)
            #time.sleep(5)
            GPIO.output(23, False)
        else:
            if ID == Tag2:
                print("matched 2:  ",now)
                GPIO.output(23, True)
                GPIO.output(24, False)
                #time.sleep(5)
                GPIO.output(23, False)
            else:
                GPIO.output(23, False)
                print("Access Denied")
                GPIO.output(24, True)
                #time.sleep(5)
                GPIO.output(24, False)