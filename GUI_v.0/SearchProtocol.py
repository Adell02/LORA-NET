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

def SendSearch(ser,respondToId):
    sendSearch = bytes(str(respondToId) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER + searchString + config.END_MARKER,encoding="UTF-8")
    ser.write(sendSearch)

def PrintResult(textBox):
    with zipfile.ZipFile(config.IN_SEARCH_URL,"r",zipfile.ZIP_DEFLATED) as file:
        textBox.write("Results returned: ")
        textBox.write(file.read('search.txt').decode())


def SendSearchResults(ser,file,toID,textBox):
        # Header of every packet
    header = str(toID) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER 
    print(file.filename)
    # Check the file size and number of packets to send
    filesize = os.path.getsize(file.filename)
    if (filesize % config.FILE_SPLIT == 0):
        packets = int(filesize / config.FILE_SPLIT)
    else:
        packets = int(filesize / config.FILE_SPLIT + 1)
    textBox.write("\n Sending %i bytes in %i packets." % (filesize, packets))


    # Read the file
    with open(file.filename, 'rb') as f:
        message = f.read()
    binary_data = ""
    i = 0
    j = 0

    # Inform to the receiver the type of message we are sending (FILE) + ID in header
    ser.write(bytes(header +"FILE"+config.END_MARKER, encoding="utf8"))
    sleep(2)
    for m in message:
        
        # Append in a string character by character until we have "config.FILE_SPLIT" characters
        binary_data += str(m) + " "
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
    textBox.write("Sent Successfully")

    

def WebScraping(ser,searchToDo,toId, textBox):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    searchToDo = "https://www.google.com/search?q=" + searchToDo.replace(" ","+") + "&num=15"
    browser = webdriver.Chrome("./chromedriver.exe",chrome_options=options)
    browser.implicitly_wait(10)
    browser.get(searchToDo)
    browser.find_element_by_id('L2AGLb').click()
    h3 = browser.find_elements_by_class_name('LC20lb')
    link = browser.find_elements_by_tag_name('cite')
    text = browser.find_elements_by_class_name('VwiC3b')

    txt =""
    if(len(h3)== len(link)/2== len(text)):
                for i in range(len(h3)):
                    txt += link[i*2].text+'\n'+h3[i].text+'\n'+ text[i].text +'\n-----\n'

    #with tempfile.TemporaryFile() as tmp:
    #    zf = zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
    #    zf.writestr('search.txt',txt )
    #    tmp.seek(0)
    #    zf.close()
    #    SendSearchResults(ser,zf,toId,textBox)
    zf = zipfile.ZipFile(config.IN_SEARCH_URL,'w',zipfile.ZIP_DEFLATED)
    zf.writestr('search.txt',txt )
    zf.close()
    SendSearchResults(ser,zf,toId,textBox)
    

