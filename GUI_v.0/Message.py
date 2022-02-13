import sys
from time import sleep
import config

def SendMg(ser,mg,textBox):
    mgsize = sys.getsizeof(mg)
    if (mgsize%config.MG_SPLIT == 0):
        packets = mgsize//config.MG_SPLIT
    else: 
        packets = mgsize//config.MG_SPLIT +1      
    textBox.write("\n Sending %i bytes in %i packets." %(mgsize, packets))
    ser.write(bytes("MG"+config.END_MARKER,encoding="UTF8"))
    sleep(2)
    i=0
    if (sys.getsizeof(mg)<(config.MG_SPLIT-1)):        
        ser.write(bytes(mg+config.END_MARKER, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
        textBox.write("Packet %i" %(i))
        textBox.PB_step(100/packets,0)
        sleep(1)
    else:
        mg_split = ""
        while(i <= sys.getsizeof(mg)//(config.MG_SPLIT-1)):
            mg_split = mg[i*(config.MG_SPLIT-1):(config.MG_SPLIT-1)+i*(config.MG_SPLIT-1)] + config.END_MARKER
            ser.write(bytes(mg_split, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
            textBox.write("Packet %i" %(i))
            textBox.PB_step(100/packets,0)
            i+=1
            sleep(2)


    sleep(2)
    ser.write(bytes("END"+config.END_MARKER, encoding="utf8"))    # End of transmission alert for receiver
    textBox.PB_step(0,1)
