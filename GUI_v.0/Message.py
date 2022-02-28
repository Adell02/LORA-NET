from distutils.log import ERROR
import sys
from time import sleep
import config

# Main send message function
def SendMg(ser, mg, ToId, textBox):
    # Header of every packet
    header =  str(ToId) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER 
    # Get max pcket size with the header
    pckt_size = config.MG_SPLIT - len(str(ToId))
    # Get byte size of the message and number of packets
    mgsize = sys.getsizeof(mg)
    packets = mgsize//pckt_size + (mgsize % pckt_size > 0)

    textBox.write("\n Sending %i bytes in %i packets." % (mgsize, packets))    
    ser.write(bytes(header + "MG"+str(packets)+config.END_MARKER, encoding="UTF8"))       
    i = 0
    mg_split = ""

    # Send all packets
    while(i <= sys.getsizeof(mg)//(pckt_size-1)):
        mg_split = mg[i*(pckt_size-1):(pckt_size-1) +
                      i*(pckt_size-1)] + config.END_MARKER
        ser.inWaiting()
        sleep(config.PCKT_SLEEP)
        ser.write(bytes(header + mg_split, encoding="utf8"))
        textBox.write("Packet %i" % (i))
        textBox.PB_step(100/packets, 0)
        i += 1

    # End of transmission alert for receiver
    ser.inWaiting()
    sleep(config.PCKT_SLEEP)
    ser.write(bytes(header + "END"+config.END_MARKER, encoding="utf8"))
    textBox.PB_step(0, 1)
    # Ensuring we don't read our own messages
    ser.readline()
