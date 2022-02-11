import sys
from time import sleep


def SendMg(ser,mg,textBox):
    mgsize = sys.getsizeof(mg)
    if (mgsize%255 == 0):
        packets = mgsize//255
    else: 
        packets = mgsize//255 +1      
    textBox.write("\n Sending %i bytes in %i packets." %(mgsize, packets))
    ser.write(bytes("MG",encoding="UTF8"))
    sleep(2)
    i=0
    if (sys.getsizeof(mg)<254):
        ser.write(bytes(mg, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
        textBox.write("Packet %i" %(i))
        textBox.PB_step(100/packets,0)
        print(mg)
        sleep(1)
    else:
        mg_split = ""
        print(sys.getsizeof(mg)//254)
        while(i <= sys.getsizeof(mg)//254):
            #start = i*254
            #end = 254 * (i+1)
            mg_split = mg[i*254:254+i*254]
            ser.write(bytes(mg_split, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
            textBox.write("Packet %i" %(i))
            textBox.PB_step(100/packets,0)
            i+=1
            sleep(2)


    sleep(2)
    ser.write(bytes("END", encoding="utf8"))    # End of transmission alert for receiver
    textBox.PB_step(0,1)
