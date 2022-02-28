from time import sleep
import os
import config

# Read the hex file and return the content
def open_file(route):
    lines = []
    with open(route, 'rb') as f:
        line = f.readline()
        while (line):
            lines.append(line)
            line = f.readline()
    return(lines)

# Main Function
def SendFile(ser, route, ToId, textBox):
    # Header of every packet
    header = str(ToId) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER 

    pckt_size = (config.FILE_SPLIT - len(str(ToId)))//4     # Each symbol is encoded into a 4byte int

    # Check the file size and number of packets to send
    filesize = os.path.getsize(route)
    packets = filesize//pckt_size + (filesize % pckt_size > 0)
    
    textBox.write("\n Sending %i bytes in %i packets." % (filesize, packets))

    # Read the file
    message = open_file(route)
    binary_data = ""
    i = 0
    j = 0

    # Inform to the receiver the type of message we are sending (FILE) + ID in header
    ser.write(bytes(header +"FILE"+str(packets)+config.END_MARKER, encoding="utf8"))
    ser.inWaiting()
    sleep(config.PCKT_SLEEP)
    for m in message:
        for car in m:
            # Append in a string character by character until we have "pckt_size" characters
            binary_data += str(car) + " "
            if(i > pckt_size):
                ser.write(bytes(header+binary_data+config.END_MARKER, encoding="utf8"))
                textBox.write("Packet %i" % (j))
                textBox.PB_step(100/packets, 0)
                # Give some time to the arduino to send it (Upgrade would be improving delay time)
                ser.inWaiting()
                sleep(config.PCKT_SLEEP)
                binary_data = ""
                i = 0
                j += 1
            i += 1

    # In case the last string has less characters than "pckt_size"
    if (binary_data != ""):
        ser.write(bytes(header+binary_data+config.END_MARKER, encoding="utf8"))
        textBox.write("Packet %i" % (j))
        textBox.PB_step(100/packets, 0)

    # Sending last message "END" to inform the receiver
    ser.inWaiting()
    sleep(config.PCKT_SLEEP)
    ser.write(bytes(header+"END"+config.END_MARKER, encoding="utf8"))
    textBox.PB_step(0, 1)
    ser.readline()
