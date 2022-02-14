from re import search
from time import sleep
from tkinter import StringVar
import config

# Sends the request to all Nodes
def SendRequest(ser,search):
    global searchString
    searchString = search
    request =  str(config.ALL_ID) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER + "GS"+config.END_MARKER
    ser.write(bytes(request,encoding="UTF-8"))

def SendSearch(ser,respondToId):
    sendSearch = bytes(str(respondToId) + config.FROM_TO_MARKER + str(config.ID) + config.ID_MARKER + searchString + config.END_MARKER,encoding="UTF-8")
    ser.write(sendSearch)

def WebScrapping(ser,searchToDo):
    pass

