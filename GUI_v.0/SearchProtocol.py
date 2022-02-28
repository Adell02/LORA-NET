from email import message
import os
from time import sleep
import config
from selenium import webdriver
import tempfile
import zipfile

import FileExporterOne

# Sends the request to all Nodes
def SendRequest(ser,search):
    global searchString
    searchString = search
    request =  str(config.ALL_ID) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER + "GS"+config.END_MARKER
    ser.write(bytes(request,encoding="UTF-8"))

def SendSearch(ser,respondToID):
    sendSearch = bytes(str(respondToID) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER + searchString + config.END_MARKER,encoding="UTF-8")
    ser.write(sendSearch)

def PrintResult(textBox):
    with zipfile.ZipFile(config.IN_SEARCH_URL,"r",zipfile.ZIP_DEFLATED) as file:
        textBox.write("\nResults returned: ")
        textBox.write(file.read('search.txt').decode())


def SendSearchResults(ser,file,ToID,textBox):
    # Header of every packet
    header = str(ToID) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER 

    pckt_size = (config.FILE_SPLIT - len(str(ToID)))//4     # Each symbol is encoded into a 4byte int

    # Check the file size and number of packets to send
    filesize = os.path.getsize(file.filename)
    packets = filesize//pckt_size + (filesize % pckt_size > 0)

    textBox.write("\n Sending %i bytes in %i packets." % (filesize, packets))


    # Read the file
    with open(file.filename, 'rb') as f:
        message = f.read()
    binary_data = ""
    i = 0
    j = 0

    # Inform to the receiver the type of message we are sending (FILE) + ID in header
    ser.write(bytes(header +"FILE"+config.END_MARKER, encoding="utf8"))
    ser.inWaiting()
    sleep(config.PCKT_SLEEP)
    for m in message:        
        # Append in a string character by character until we have "pckt_size" characters
        binary_data += str(m) + " "
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
    textBox.write("Sent Successfully")

    

def WebScraping(ser,searchToDo,ToID, textBox):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    searchToDo = "https://www.google.com/search?q=" + searchToDo.replace(" ","+") + "&num=15"
    browser = webdriver.Chrome("./chromedriver.exe",chrome_options=options)
    browser.implicitly_wait(10)
    browser.get(searchToDo)
    browser.find_element_by_id('L2AGLb').click()
    h3 = browser.find_elements_by_class_name('LC20lb')
    link = browser.find_elements_by_class_name('tjvcx')
    text = browser.find_elements_by_class_name('VwiC3b')

    txt =""
    links=[]

    for l in link:
            if l.text!="":
                    links.append(l)
    for i in range(len(h3)-1):
            txt += links[i].text+'\n'+h3[i].text+'\n'+ text[i].text +'\n-----\n'
 
    print(txt)
    #with tempfile.TemporaryFile() as tmp:
    #    zf = zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
    #    zf.writestr('search.txt',txt )
    #    tmp.seek(0)
    #    zf.close()
    #    SendSearchResults(ser,zf,ToID,textBox)
    zf = zipfile.ZipFile(config.IN_SEARCH_URL,'w',zipfile.ZIP_DEFLATED)
    zf.writestr('search.txt',txt )
    zf.close()
    SendSearchResults(ser,zf,ToID,textBox)
    

