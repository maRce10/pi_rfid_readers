
import time
import serial
from datetime import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

message=str('')
lastSignal = 0
transmission = False
state = 0
pos=0

GREENPIN = 10
REDPIN = 9

dishka = 8
dishkaFake = 1532661448

lastSignal = datetime.now()

GPIO.setup(GREENPIN, GPIO.OUT)
GPIO.setup(REDPIN, GPIO.OUT)
GPIO.output(GREENPIN, False)
GPIO.output(REDPIN, False)

PortFP = serial.Serial('/dev/ttyAMAO', 9600)
print("Start")

def hexInDec(message, beg , length):
    mult = 1
    nbr = 0
    i = beg
    while (i < beg + length):
        nextInt = int(message[i])
        if (nextInt >= 48 & nextInt <= 57):
            nextInt = map(nextInt, 48, 57, 0, 9)
        if (nextInt >= 65 & nextInt <= 70):
            nextInt = map(nextInt, 65, 70, 10, 15)
        if (nextInt >= 97 & nextInt <= 102):
            nextInt = map(nextInt, 97, 102, 10, 15)
        nextInt = constrain(nextInt, 0, 15)
        nbr = nbr + (mult * nextInt)
        mult = mult * 16
        i=i+1
    return nbr



while True:
    
    ID_read = ''
    read_byte = PortRF.read().decode("utf-8")
    if read_byte == "\x02":
        for Counter in range(12):
            read_byte = PortRF.read()
            ID_read = ID_read + str(read_byte)
            #print(hex(ord(read_byte)))
        ID_read = ID_read.replace("b","").replace("'","")
        ID_read = int(ID_read)
        print(ID_read)
        now = datetime.now()
    
    state = {
        
        1:
            if (ID_read > 0):
                lastSignal = datetime.now()
                pos = 0
                state = 2
                
            break;
            
        
        2:{
            if (Serial2.available() > 0 && pos < 35) {
                lastSignal = datetime.now()
                message[pos] = Serial2.read()
                //               print(message[pos], HEX)
                //               print(",")
                pos+=1
                }
            if (datetime.now() - lastSignal > 100) {
                state = 3
                }
            if (pos >= 35) {
                time.sleep(5)
                state = 1
                }
            }
        break
        
        3:{
            // checksum
            print()
            check = message[1]
            for (int i = 2; i < 27; i++) {
                check = check ^ message[i]
                }
            print()
            //      print(check);
            //      print(",");
            //      print(message[27], HEX);
            if (check == message[27]) {
                //        print("Check OK");
                
                // Decodung
                ID = hexInDec(message, 1, 10)
                countryNbr = hexInDec(message, 11, 4)
                
                print("CardNumber=")
                print(ID)
                print("Country=")
                print(countryNbr)
                
                if (ID == dishka || ID == dishkaFake) {
                    GPIO.output(GREENPIN, False)
                    GPIO.output(REDPIN, True)
                    print("It is Dishka!")
                    } else {
                        GPIO.output(GREENPIN, True)
                        GPIO.output(REDPIN, False)
                        print("It is not Dishka!")
                        }
                state = 4
                }
            break
            }
        
        4:{
            time.sleep(5)
            GPIO.output(GREENPIN, True)
            GPIO.output(REDPIN, True)
            state = 1
            break
            }
        
        5: lambda: print("Caso no contemplado")
        }
    