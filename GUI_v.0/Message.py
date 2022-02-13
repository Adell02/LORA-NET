import sys
from time import sleep
import config

# Main send message function
def SendMg(ser,mg,textBox):

    # Get byte size of the message and number of packets
    mgsize = sys.getsizeof(mg)
    if (mgsize%config.MG_SPLIT == 0):
        packets = mgsize//config.MG_SPLIT
    else: 
        packets = mgsize//config.MG_SPLIT +1      
    textBox.write("\n Sending %i bytes in %i packets." %(mgsize, packets))
    ser.write(bytes(str(config.ID)+config.ID_MARKER+"MG"+config.END_MARKER,encoding="UTF8"))
    sleep(2)
    i=0
    mg_split = ""

    # Send all packets
    while(i <= sys.getsizeof(mg)//(config.MG_SPLIT-1)):
        mg_split = mg[i*(config.MG_SPLIT-1):(config.MG_SPLIT-1)+i*(config.MG_SPLIT-1)] + config.END_MARKER
        ser.write(bytes(str(config.ID)+config.ID_MARKER+mg_split, encoding="utf8"))      # Sends string of 61 integers = 244 bytes (4 x int) 
        textBox.write("Packet %i" %(i))
        textBox.PB_step(100/packets,0)
        i+=1
        sleep(2)


    sleep(2)
    ser.write(bytes(str(config.ID)+config.ID_MARKER+"END"+config.END_MARKER, encoding="utf8"))    # End of transmission alert for receiver
    textBox.PB_step(0,1)
