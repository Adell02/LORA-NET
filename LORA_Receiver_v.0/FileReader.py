from asyncore import read
from time import sleep
from numpy import r_
import serial
import binascii

ser = serial.Serial(port='COM5', baudrate = 9600, timeout=.1)   #open serial port
doc = './LORA_Receiver_v.0/received_file.rar'

with open (doc,'w') as f:   # Blank document
    f.write('')

def open_file(read):    # Appends in hex data in document
    #print(type(read))
    try:
        r_str = read.decode()
        r_arr = r_str.split()
        for i in range(0,len(r_arr)):
            r_arr[i] = '{:02x}'.format(int(r_arr[i],10),'x')
            #print(r_arr[i])
            r_arr[i] = binascii.unhexlify(r_arr[i])
    
        #print(r_arr)
        with open (doc,'ab') as f:
            for wr in r_arr:
                f.write(wr)
    except:
        pass
counter  =0
while (True):
    a_read = ser.readline()
    #print(a_read)
    if(len(a_read) and a_read != b"END"):
        print(counter)
        print(a_read)
        open_file(a_read)
        counter+=1
    elif(a_read == b"END"):
        break




        




          
