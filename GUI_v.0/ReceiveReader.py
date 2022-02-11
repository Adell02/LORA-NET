import binascii
from email import message
from tkinter import *


doc = 'received_file.rar'

# Set RECEIVING indicator
def SetReceivingLight(textBox):
    if(textBox.indicator.get() == 0):
        textBox.radioReceiving['state'] = NORMAL
        textBox.indicator.set(2)
        textBox.radioReceiving['fg'] = 'green'        

    else:
        textBox.indicator.set(0)
        textBox.radioReceiving['fg'] = 'gray'
        textBox.radioReceiving['state'] = DISABLED

# Read message between start and end
def ReadUntilEnd(ser):
    message = ""
    a_read = ser.readline()
    while(a_read!= b"END"):        
        if(len(a_read)):
            message += a_read.decode()        
        a_read = ser.readline()
    return(message)

# Appends hex data in document
def open_file(ser,textBox,error_list):   
    a_read = ser.readline()
    index = 0
    while(a_read!= b"END"):        
        if(len(a_read)):
            textBox.write("Packet %i" %(index))
            a_read = a_read.decode()                            
            try:
                r_arr = a_read.split()
                for i in range(0,len(r_arr)):
                    r_arr[i] = '{:02x}'.format(int(r_arr[i],10),'x')
                    r_arr[i] = binascii.unhexlify(r_arr[i])

                with open (doc,'ab') as f:
                    for wr in r_arr:
                        f.write(wr)
            except:
                error_list.append(index)
            index += 1            
        a_read = ser.readline()


def ContinuousReader(ser,textBox):
    textBox.write("\n Continuous Reading Enabled")
    while (True):    
        a_read = ser.readline()
        if(len(a_read) and textBox.indicator.get()==0):         
            SetReceivingLight(textBox)               
            if (a_read == b"GS"):
                continue
            elif (a_read == b"MG"):
                textBox.write("\n Message incoming: ")
                textBox.write(ReadUntilEnd(ser))
            elif (a_read == b"FILE"):
                with open (doc,'w') as f:   # Blank document
                    f.write('')
                error_list=[]
                textBox.write("\n File Incoming: ")
                open_file(ser,textBox,error_list)
                textBox.write("File Received with %i errors" %(len(error_list)))

            SetReceivingLight(textBox)   




        




          
