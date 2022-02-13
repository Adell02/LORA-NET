from base64 import encode
import binascii
from logging import root
from tkinter import *
import config

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

# Read message between start and end checking ID on every packet
def ReadUntilEnd(ser, header):
    message = ""
    a_read = ser.readline()
    while(a_read != header + bytes(config.ID_MARKER,encoding="UTF-8") + b"END"):
        if(len(a_read) and a_read.split(bytes(config.ID_MARKER, encoding="UTF-8"))[0] == header):
            message += (a_read.decode()).replace(header.decode()+config.ID_MARKER, "")
        a_read = ser.readline()
    return(message)

# Writes hex data in blank document checking ID on every packet
def open_file(ser, textBox, header, error_list):
    with open(config.IN_FILE_URL, 'w') as f:
        f.write('')
    a_read = ser.readline()
    index = 0
    while(a_read != header + b"END"):
        if(len(a_read) and a_read.split(bytes(config.ID_MARKER, encoding="UTF-8"))[0] == header):
            textBox.write("Packet %i" % (index))
            a_read = a_read.decode().replace(header.decode(), "")

            # Try to convert read into hex string (if not possible, packet received wrongly => add the index of that packet to error_list)
            try:
                r_arr = a_read.split()
                for i in range(0, len(r_arr)):
                    r_arr[i] = '{:02x}'.format(int(r_arr[i], 10), 'x')
                    r_arr[i] = binascii.unhexlify(r_arr[i])

                with open(config.IN_FILE_URL, 'ab') as f:
                    for wr in r_arr:
                        f.write(wr)
            except:
                error_list.append(index)
            index += 1
        a_read = ser.readline()

# Main Continuous reading function
def ContinuousReader(ser, textBox):

    while (root):
        a_read = ser.readline()
        if(b"READY" in a_read):
            textBox.write("\n Node Ready")
            textBox.write("Continuous Reading Enabled")

        elif(len(a_read) and textBox.indicator.get() == 0):
            try:
                # Get the ID from the message incomming
                header = a_read.split(bytes(config.ID_MARKER, encoding="UTF-8"))[0]
                ToId = int(header.split(bytes(config.FROM_TO_MARKER,encoding="UTF-8"))[0])
                FromId = int(header.split(bytes(config.FROM_TO_MARKER,encoding="UTF-8"))[1])
            except:
                pass    # Wrong packet with no header, just ignore

            # if(FromId != config.ID):       DISABLED FOR DEBBUGING
            SetReceivingLight(textBox)
            if (b"GS" in a_read and ToId == config.ID):
                continue
            elif (b"MG" in a_read and ToId == config.ID):
                textBox.write("\n Message incoming from User Node %i: " % (FromId))
                textBox.write(ReadUntilEnd(ser, header))
            elif (b"FILE" in a_read and ToId == config.ID):
                error_list = []
                textBox.write("\n File Incoming from User Node %i: " % (FromId))
                open_file(ser, textBox, header, error_list)
                textBox.write("File Received with %i errors" %
                              (len(error_list)))

            SetReceivingLight(textBox)
