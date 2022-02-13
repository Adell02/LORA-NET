from base64 import encode
import binascii
from tkinter import *
import config


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
def ReadUntilEnd(ser,Id):
    IdTag = bytes(str(Id)+config.ID_MARKER,encoding="UTF-8")
    message = ""    
    a_read = ser.readline()
    while(a_read!= IdTag+b"END"):   

        if(len(a_read) and a_read.split(bytes(config.ID_MARKER,encoding="UTF-8"))[0] == bytes(str(Id),encoding="UTF-8")):
            message += (a_read.decode()).replace(IdTag.decode(),"")
        a_read = ser.readline()
    return(message)

# Appends hex data in document
def open_file(ser,textBox,Id,error_list):  
    IdTag = bytes(str(Id)+config.ID_MARKER,encoding="UTF-8")
    a_read = ser.readline()        
    index = 0
    while(a_read!= IdTag+b"END"):        
        if(len(a_read) and a_read.split(bytes(config.ID_MARKER,encoding="UTF-8"))[0] == bytes(str(Id),encoding="UTF-8")):
            textBox.write("Packet %i" %(index))
            a_read = a_read.decode().replace(IdTag.decode(),"")                            
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
        if(b"READY" in a_read):
            textBox.write("Node Ready.")                        
            
        elif(len(a_read) and textBox.indicator.get()==0):  
            Id = int(a_read.split(bytes(config.ID_MARKER,encoding="UTF-8"))[0])
            #if(Id != config.ID):       DISABLED FOR DEBBUGING
            
            SetReceivingLight(textBox)               
            if (b"GS" in a_read):
                continue
            elif (b"MG" in a_read):
                textBox.write("\n Message incoming from User Node %i: " %(Id))
                textBox.write(ReadUntilEnd(ser,Id))
            elif (b"FILE"in a_read):
                with open (doc,'w') as f:   # Blank document
                    f.write('')
                error_list=[]
                textBox.write("\n File Incoming from User Node %i: " %(Id))
                open_file(ser,textBox,Id,error_list)
                textBox.write("File Received with %i errors" %(len(error_list)))

            SetReceivingLight(textBox)   




        




          
