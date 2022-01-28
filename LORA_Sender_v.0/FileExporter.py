from time import sleep
import serial
import binascii

ser = serial.Serial(port='COM3', baudrate = 9600, timeout=.1)   #open serial port

def open_file():    #makes a large string with all the data in the file
    lines = []
    with open ('./LORA_Sender_v.0/close_ejemplo_2kb.rar','rb') as f:
        line = f.readline()
        
        while (line):
            lines.append(line)
            line= f.readline()            
    return(lines)   

message = open_file()
print(message)
binary_data = ""
i=0
j=0
sleep(2)
for m in message:
    for car in m:
        binary_data += str(car) + " "  # Turns the caracters into binary
        if(i>24):
            ser.write(bytes(binary_data, encoding="utf8"))      # Sends string of 25 characters = 250 bytes (8 x character + 2 x character -> 0b at beginning) 
            print(j)
            print(binary_data)
            print()
            sleep(2.5)        # Give some time to the arduino to send it (trying to send it simultaneously)
            binary_data = ""
            i = 0
            j+=1
        i+=1
if (binary_data != ""):         # In case the last string is <24 chars
    ser.write(bytes(binary_data, encoding="utf8"))      
    print(j)
    print(binary_data)

sleep(2)
ser.write(bytes("END", encoding="utf8"))    # End of transmission alert for receiver
          
