import sys
from time import sleep
import config

# Main send message function
def SendMg(ser, mg, ToId, textBox):
    # Header of every packet
    header =  str(ToId) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER 
    # Get byte size of the message and number of packets
    mgsize = sys.getsizeof(mg)
    if (mgsize % config.MG_SPLIT == 0):
        packets = mgsize//config.MG_SPLIT
    else:
        packets = mgsize//config.MG_SPLIT + 1
    textBox.write("\n Sending %i bytes in %i packets." % (mgsize, packets))
    ser.write(bytes(header + "MG"+config.END_MARKER, encoding="UTF8"))
    sleep(2)
    i = 0
    mg_split = ""

    # Send all packets
    while(i <= sys.getsizeof(mg)//(config.MG_SPLIT-1)):
        mg_split = mg[i*(config.MG_SPLIT-1):(config.MG_SPLIT-1) +
                      i*(config.MG_SPLIT-1)] + config.END_MARKER
        ser.write(bytes(header + mg_split, encoding="utf8"))
        textBox.write("Packet %i" % (i))
        textBox.PB_step(100/packets, 0)
        i += 1
        sleep(2)

    # End of transmission alert for receiver
    sleep(2)
    ser.write(bytes(header + "END"+config.END_MARKER, encoding="utf8"))
    textBox.PB_step(0, 1)
