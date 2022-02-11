from time import sleep
import os

def open_file(route):    #makes a large string with all the data in the file
    lines = []
    with open (route,'rb') as f:
        line = f.readline()
        
        while (line):
            lines.append(line)
            line= f.readline()            
    return(lines)   

def SendMain(ser,route,textBox):
    filesize = os.path.getsize(route)
    if (filesize%62 == 0):
        packets = int(filesize / 62)
    else: 
        packets = int(filesize / 62 + 1)        
    textBox.write("\n Sending %i bytes in %i packets." %(filesize, packets))
    message = open_file(route)
    print(message)
    binary_data = ""
    i=0
    j=0
    ser.write(bytes("FILE",encoding="utf8"))
    sleep(2)
    for m in message:
        for car in m:
            binary_data += str(car) + " "  # Turns the caracters into binary
            if(i>62):
                ser.write(bytes(binary_data, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
                #print(j)
                print(binary_data)
                #print()
                textBox.write("Packet %i" %(j))
                textBox.PB_step(100/packets,0)
                sleep(2.5)        # Give some time to the arduino to send it (trying to send it simultaneously)
                binary_data = ""
                i = 0
                j+=1
            i+=1
    if (binary_data != ""):         # In case the last string is <24 chars
        ser.write(bytes(binary_data, encoding="utf8"))      
        #print(j)
        print(binary_data)
        textBox.write("Packet %i" %(j))
        textBox.PB_step(100/packets,0)

    sleep(2)
    ser.write(bytes("END", encoding="utf8"))    # End of transmission alert for receiver
    textBox.PB_step(0,1)

