from time import sleep
import os
import config

def open_file(route):    #makes a large string with all the data in the file
    lines = []
    with open (route,'rb') as f:
        line = f.readline()
        
        while (line):
            lines.append(line)
            line= f.readline()            
    return(lines)   

def SendFile(ser,route,textBox):
    filesize = os.path.getsize(route)
    if (filesize%config.FILE_SPLIT == 0):
        packets = int(filesize / config.FILE_SPLIT)
    else: 
        packets = int(filesize / config.FILE_SPLIT + 1)        
    textBox.write("\n Sending %i bytes in %i packets." %(filesize, packets))
    message = open_file(route)
    print(message)
    binary_data = ""
    i=0
    j=0
    ser.write(bytes("FILE"+config.END_MARKER,encoding="utf8"))
    sleep(2)
    for m in message:
        for car in m:
            binary_data += str(car) + " "  # Turns the caracters into binary
            if(i>config.FILE_SPLIT):
                ser.write(bytes(binary_data+config.END_MARKER, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
                print(binary_data)
                textBox.write("Packet %i" %(j))
                textBox.PB_step(100/packets,0)
                sleep(2.5)        # Give some time to the arduino to send it (trying to send it simultaneously)
                binary_data = ""
                i = 0
                j+=1
            i+=1
    if (binary_data != ""):         # In case the last string is <24 chars
        ser.write(bytes(binary_data+config.END_MARKER, encoding="utf8"))      
        print(binary_data)
        textBox.write("Packet %i" %(j))
        textBox.PB_step(100/packets,0)

    sleep(2)
    ser.write(bytes("END"+config.END_MARKER, encoding="utf8"))    # End of transmission alert for receiver
    textBox.PB_step(0,1)

