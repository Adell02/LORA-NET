from unittest import case
from tkinter import *

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
    a_read = ser.readline()
    while(a_read!= b"END"):
        a_read = ser.readline()
        if(len(a_read)):
            return(a_read.decode())


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
                continue
            SetReceivingLight(textBox)   




        




          
