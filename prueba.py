
from ast import While
from distutils.command.config import config
from tokenize import String
from selenium import webdriver
import zipfile
import tempfile
import serial


#url = 'https://www.google.com/search?q=Github&num=20'
#options = webdriver.ChromeOptions()
##options.add_argument('headless')
#browser = webdriver.Chrome("./chromedriver.exe",chrome_options=options)
#browser.implicitly_wait(10)
#browser.get(url)
#browser.find_element_by_id('L2AGLb').click()
#h3 = browser.find_elements_by_class_name('LC20lb')
#link = browser.find_elements_by_class_name('tjvcx')
#text = browser.find_elements_by_class_name('VwiC3b')
#links=[]
#
#for l in link:
#        if l.text!="":
#                links.append(l)
#
#txt =""
#for i in range(len(h3)-1):
#        txt += links[i].text+'\n'+h3[i].text+'\n'+ text[i].text +'\n-----\n'
#
#with zipfile.ZipFile("received_results_GS.zip",'w',zipfile.ZIP_DEFLATED) as zf:
#    zf.writestr('search.txt',txt )
 

#######        
#zf = zipfile.ZipFile("read.zip", mode="w", compression=zipfile.ZIP_DEFLATED)

#zf.close()
#zf = zipfile.ZipFile("read.zip")

#######
#with zipfile.ZipFile("received_results_GS.zip","r",zipfile.ZIP_DEFLATED) as file:
#        print("Results returned: ")
#        print(file.read('search.txt').decode())

import sys
from time import sleep


# Main send message function
def SendMg(ser, mg):
    mgsplit = 260

    mgsize = sys.getsizeof(mg)
    if (mgsize % mgsplit == 0):
        packets = mgsize//mgsplit
    else:
        packets = mgsize//mgsplit + 1
    
    print("\n Sending %i bytes in %i packets." % (mgsize, packets))
    i = 0
    mg_split = ""

    # Send all packets
    while(i <= sys.getsizeof(mg)//(mgsplit-1)):
        mg_split = mg[i*(mgsplit-1):(mgsplit-1) +
                      i*(mgsplit-1)] + "*"
        ser.inWaiting()
        sleep(0.45)
        ser.write(bytes(mg_split, encoding="utf8"))
        print("Sending %i packet"%(i))
        i += 1




    
ser = serial.Serial(port='COM3',baudrate=9600, timeout=.1)
while(ser):
        print("Enter msg: ")
        msg = "\n\nI've got a Python program which is reading data from a serial port via the PySerial module. The two conditions I need to keep in mind are: I don't know how much data will arrive, and I don't know when to expect data. \n I've got a Python program which is reading data from a serial port via the PySerial module. The two conditions I need to keep in mind are: I don't know how much data will arrive, and I don't know when to expect data.\n I've got a Python program which is reading data from a serial port via the PySerial module. The two conditions I need to keep in mind are: I don't know how much data will arrive, and I don't know when to expect data."
        if input():
                SendMg(ser,msg)

