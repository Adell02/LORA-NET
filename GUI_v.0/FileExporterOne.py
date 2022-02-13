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

    # Check the file size and number of packets to send
    filesize = os.path.getsize(route)
    if (filesize % config.FILE_SPLIT == 0):
        packets = int(filesize / config.FILE_SPLIT)
    else:
        packets = int(filesize / config.FILE_SPLIT + 1)
    textBox.write("\n Sending %i bytes in %i packets." % (filesize, packets))

    # Read the file
    message = open_file(route)
    binary_data = ""
    i = 0
    j = 0

    # Inform to the receiver the type of message we are sending (FILE) + ID in header
    ser.write(bytes(header +"FILE"+config.END_MARKER, encoding="utf8"))
    sleep(2)
    for m in message:
        for car in m:
            # Append in a string character by character until we have "config.FILE_SPLIT" characters
            binary_data += str(car) + " "
            if(i > config.FILE_SPLIT):
                ser.write(bytes(header+binary_data+config.END_MARKER, encoding="utf8"))
                textBox.write("Packet %i" % (j))
                textBox.PB_step(100/packets, 0)
                # Give some time to the arduino to send it (Upgrade would be improving delay time)
                sleep(2.5)
                binary_data = ""
                i = 0
                j += 1
            i += 1

    # In case the last string has less characters than "config.FILE_SPLIT"
    if (binary_data != ""):
        ser.write(bytes(header+binary_data+config.END_MARKER, encoding="utf8"))
        textBox.write("Packet %i" % (j))
        textBox.PB_step(100/packets, 0)

    # Sending last message "END" to inform the receiver
    sleep(2)
    ser.write(bytes(header+"END"+config.END_MARKER, encoding="utf8"))
    textBox.PB_step(0, 1)
