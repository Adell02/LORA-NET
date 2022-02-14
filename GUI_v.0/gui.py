import sys
import threading
from tkinter import filedialog
from tkinter.ttk import Progressbar
import webbrowser
import PIL.Image
import PIL.ImageTk
import serial
import urllib.request
from tkinter import *

import SearchProtocol
from FileExporterOne import SendFile
from Message import SendMg
from ReceiveReader import ContinuousReader

import config


# Menubar functions
def SavePrompt():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(textBox.textBox.get(1.0, END))
    f.write(text2save)
    f.close()


def selectall():
    textBox.textBox.focus()
    textBox.textBox.tag_add('sel', '1.0', 'end')


def clearall():
    textBox.textBox.config(state=NORMAL)
    textBox.textBox.delete('1.0', END)
    textBox.textBox.config(state=DISABLED)


def Help():
    webbrowser.open_new('https://github.com/Adell02/LORA-NET')


def AboutLora():
    textBox.write(config.LOG)

# Open Serial Communication with Arduino reading the Port Entry on screen
def OpenCom(event):
    global ser
    ComPort.set(com.get())
    try:
        if error.get() == 0:
            textBox.write(
                "\n %s port has already been successfully configured" % (ComPort.get()))
        else:
            ser = serial.Serial(port=ComPort.get(),
                                baudrate=config.BAUDRATE, timeout=.1)
            error.set(0)
    except:
        textBox.write("%s port not set correctly." % (ComPort.get()))
        root.update_idletasks()
        comButton.wait_variable(error)
        root.update_idletasks()

# Set the user you want to send the messages/files
def SetToId(event):
    global ToId
    ToId = SendToEntry.get()
    try:
        ToId = int(ToId)
        textBox.write("\n Valid ID. Messages will be sent to the User Node with ID: %i." %(ToId))
    except ValueError or TypeError:
        textBox.write("Please enter a valid ID (for example: 5)")

# Check if there is internet connection
def CheckInternet(set):
    url = "https://github.com/Adell02/LORA-NET"
    try:
        urllib.request.urlopen(url)                   
        if set and textBox.shareInternetStatus.get() == 0:            
            textBox.shareInternetStatus.set(1)            
            shareInternet['fg'] = "green"
            textBox.write("\n You are now sharing Internet to other User Nodes")
        elif set and textBox.shareInternetStatus.get() == 1:
            textBox.shareInternetStatus.set(0)
            shareInternet['fg'] = "black"
            textBox.write("\n You stopped sharing Internet to other User Nodes")

        elif not set and textBox.shareInternetStatus.get() == 0:
            shareInternet['state']=NORMAL
            shareInternet['fg']="black"
            is_internet.set(1)
        return(True)     
    except:
        shareInternet['state'] = DISABLED
        shareInternet['fg'] = "gray"
        textBox.shareInternetStatus.set(0)
        is_internet.set(0)
        return(False)

# Internet connection check parallel routine
def CheckInternetLoop():
    prevstatus = is_internet.get()
    CheckInternet(False)
    #root.after(500,CheckInternetLoop)
    if (prevstatus != is_internet.get() and is_internet.get()==1):
        textBox.write("\n You have internet connection now")
    elif(prevstatus != is_internet.get() and is_internet.get()==0):
        textBox.write("\n You don't have internet connection now. Sharing internet is disabled")

# Set SENDING indicator light on/off
def SetSendingLight():
    if(textBox.indicator.get() == 0):
        radioSending['state'] = NORMAL
        textBox.indicator.set(1)
        radioSending['fg'] = 'green'

    else:
        textBox.indicator.set(0)
        radioSending['fg'] = 'gray'
        radioSending['state'] = DISABLED

#  Error handling (ToID not declared, ser not declared...)      
def beforeSending(need_ToId):
    is_ToId = "ToId" in globals()
    if is_ToId:
        is_ToId = ToId
    is_ser = "ser" in globals()
    if not is_ser:
        textBox.write("You must set the Serial Port to connect to the Arduino Board first")
    elif not is_ToId and need_ToId:
        textBox.write("You must set a receiver ID")
    else:
        return(True)
    return(False)

# Function to request Internet search
def GoogleSearch(event):
    if(beforeSending(False)):
        search = Searchtxt.get()
        Searchtxt.delete(0,'end')
        if (sys.getsizeof(search)>0 and sys.getsizeof(search)<config.MG_SPLIT):
            if(config.END_MARKER in search or config.FROM_TO_MARKER in search or config.ID_MARKER in search):
                textBox.write("The search can't contain '%c', '%c' or '%c'" %(config.END_MARKER,config.FROM_TO_MARKER,config.ID_MARKER))                    
            else:            
                try:
                    SetSendingLight()
                    textBox.write("\n Sending request to other Nodes...")
                    root.after(0,SearchProtocol.SendRequest(ser,search))
                    SetSendingLight()
                    textBox.callbackStatus.set(1)
                
                except:
                    textBox.write("Something went wrong.")
        elif(sys.getsizeof(search)>config.MG_SPLIT):
            textBox.write("Consider reducing the length of the search word/sentence")
        else:
            textBox.write("You must write something.")


# Function for sending files
def SendDoc():
    if(beforeSending(True)):
        SetSendingLight()      
        route = filedialog.askopenfilename()
        try:
            SetSendingLight()
            # Function with the file sending procedure without blocking the interface (thanks to root.after)
            textBox.write(route)
            root.after(0, SendFile(ser, route, ToId, textBox))
            textBox.write("Sent Successfully")
            SetSendingLight()


        except:
            textBox.write("Sending file cancelled")

# Function for sending a Private Message
def SendMessage(event):    
    if(beforeSending(True)):
        mg = Chatmg.get()
        # Erase the entry after sending a message
        Chatmg.delete(0, 'end')    
        # Error handling (ToID not declared, ser not declared, empty message...)
        if(len(mg)>0):
            if(config.END_MARKER in mg or config.FROM_TO_MARKER in mg or config.ID_MARKER in mg):
                textBox.write("The message can't contain '%c', '%c' or '%c'" %(config.END_MARKER,config.FROM_TO_MARKER,config.ID_MARKER))                    
            else:            
                try:
                    SetSendingLight()
                    # Function with the message sending procedure  
                    textBox.write("\n Message: %s" % (mg))            
                    root.after(0, SendMg(ser, mg, ToId, textBox))
                    textBox .write("Sent successfully")    
                    SetSendingLight()
                
                except:
                    textBox.write("Something went wrong.")
        else:
            textBox.write("You must write something.")


# TEXTBOX class to use in other files such as receiving and sending ones.
class TEXTBOX:
    def __init__(self, root=None):
        self.textBoxFrame = Frame(root)
        self.textBoxFrame.pack(expand=True)

        self.textBox = Text(self.textBoxFrame, bd=1,
                            relief="solid", wrap="word")
        self.textBox.pack(side=LEFT, expand=TRUE)

        self.progressbar = Progressbar(root, length=620)
        self.progressbar.pack(expand=True)

        self.indicator = IntVar(None, 0)
        self.radioReceiving = Radiobutton()

        self.shareInternetStatus = IntVar()

        self.callbackStatus = IntVar(None,0)

    # Function that prints the message to the GUI console
    def write(self, *message, end="\n", sep=" "):
        text = " "
        for item in message:
            text += "{}".format(item)
            text += sep
        text += end
        self.textBox.configure(state="normal")
        self.textBox.insert(END, text)
        self.textBox.configure(state="disabled")
        self.textBox.see(END)
        self.textBox.update_idletasks()

    # Progress Bar steps to update it from anywhere (e.g. when sending each packet)
    def PB_step(self, step, rst):
        if not rst:
            self.progressbar['value'] += step
        else:
            self.progressbar['value'] = 0
        root.update_idletasks()


# Main window setting
root = Tk()
root.title("LoRa NET")
root.geometry("650x690")
root.resizable(0, 0)
menubar = Menu(root)
root.config(bd=15, menu=menubar)

# Menubar setting
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=SavePrompt)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear", command=clearall)
editmenu.add_command(label="Select All", command=selectall)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=Help)
helpmenu.add_separator()
helpmenu.add_command(label="About Lora Net", command=AboutLora)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

# Icon setting and main logo definition
logo = PIL.Image.open("./img/logo.png")
logo = PIL.ImageTk.PhotoImage(logo)

root.iconbitmap(r'./img/reduced_logo.ico')

# Widget definition: Frame, Title, entries + buttons, textBox
titleBox = Frame(root)
titleBox.pack(fill="both")
titleBox.columnconfigure(0, weight=1, uniform="y")
titleBox.columnconfigure(1, weight=2, uniform="y")
titleBox.columnconfigure(2, weight=1, uniform="y")

titleBox.rowconfigure(0, weight=1, uniform="x")
titleBox.rowconfigure(1, weight=1, uniform="x")
titleBox.rowconfigure(2, weight=1, uniform="x")
titleBox.rowconfigure(3, weight=1, uniform="x")
titleBox.rowconfigure(4, weight=1, uniform="x")


title = Label(titleBox, image=logo)
title.grid(row=0, column=1, sticky="nsew", rowspan=5)

SendToEntry = Entry(titleBox, width=13, justify=CENTER)
SendToEntry.grid(row=0, column=0, sticky="w")
SendToEntry.bind('<Return>',SetToId)
SendToBut = Button(titleBox, width =10,text="Receiver ID",
                   command=lambda: SetToId(True))
SendToBut.grid(row=1, column=0, sticky="w")

shareInternet = Button(titleBox, text="Share Internet",command=lambda: CheckInternet(True))
shareInternet.grid(row=3, column=0, sticky="w")

radioSending = Radiobutton(titleBox, text="Sending", fg="gray",
                           indicatoron=False, state=DISABLED, width=10, value=1)
radioSending.grid(row=0, column=2, sticky="e")

com = Entry(titleBox, width=13, justify=CENTER)
com.grid(row=3, column=2, sticky="e")
com.insert(0, config.DEFAULT_PORT)
com.bind('<Return>', OpenCom)
ComPort = StringVar()
comButton = Button(titleBox, width=10, text="Set COM",
                   command=lambda: OpenCom(True))
comButton.grid(row=4, column=2, sticky="e")


optionBox = Frame(root)
optionBox.pack(fill="x")
optionBox.columnconfigure([0, 3], weight=1)

Searchtxt = Entry(optionBox)
Searchtxt.grid(row=1, column=1, pady=5, sticky="ew")
Searchtxt.bind('<Return>',GoogleSearch)
searchBut = Button(optionBox, text="Google Search",command=lambda: GoogleSearch(True))
searchBut.grid(row=1, column=2, sticky="ew", pady=5, padx=5)

Chatmg = Entry(optionBox)
Chatmg.grid(row=2, column=1, pady=5, sticky="ew")
Chatmg.config(justify="left", state="normal")
Chatmg.bind('<Return>', SendMessage)
chatBut = Button(optionBox, text="Send Private Message",
                 command=lambda: SendMessage(True))
chatBut.grid(row=2, column=2, sticky="ew", pady=5, padx=5)

fileDir = Button(optionBox, text="Select and send file", command=SendDoc)
fileDir.grid(row=3, column=1, pady=5, sticky="ew", columnspan=2)

textBox = TEXTBOX(root)
textBox.radioReceiving = Radiobutton(titleBox, text="Receiving", fg="gray",
                                     indicatoron=False, state=DISABLED, width=10, value=2)
textBox.radioReceiving.grid(row=1, column=2, sticky="e")

radioSending['variable'] = textBox.indicator
textBox.radioReceiving['variable'] = textBox.indicator

# open serial port
error = IntVar()
error.set(1)
textBox.shareInternetStatus.set(0)
is_internet = IntVar()
if(not CheckInternet(False)):    
    textBox.write("No Internet. 'Share Internet' option disabled")
else:    
    textBox.write("Consider enabling 'Share Internet' (to other User Nodes)")

# Infinite loop checking internet connection in a secondary thread
CheckInternetLoop()

textBox.write("Please set the COM port to start using LORA net")
root.wait_variable(error)

textBox.write("%s port set correctly" % (ComPort.get()))
textBox.write(config.LOG)

# Start listening to arduino Serial in parallel thread
threading.Thread(target=ContinuousReader, args=[ser, textBox]).start()


# Destroy main window when closing app
root.protocol("WM_DELETE_WINDOW", root.destroy)

root.mainloop()
