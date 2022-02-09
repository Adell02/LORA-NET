import threading
from tkinter import filedialog
from tkinter.ttk import Progressbar
import PIL.Image
import PIL.ImageTk
import serial
from tkinter import *
from FileExporterOne import SendMain
from Message import SendMg
from ReceiveReader import ContinuousReader

root = Tk()
root.title("LoRa NET")
root.geometry("650x690")
root.resizable(0, 0)
root.config(bd=15)

logo = PIL.Image.open("./img/logo.png")
logo = PIL.ImageTk.PhotoImage(logo)

root.iconbitmap(r'./img/reduced_logo.ico')
# Open Com
def OpenCom():
    global ser    
    ComPort.set(com.get())
    try:
        if error.get() == 0:
            textBox.write("%s port has already been successfully configured" %(ComPort.get()))    
        else:
            ser = serial.Serial(port=ComPort.get(), baudrate=9600, timeout=.1)
            error.set(0)
    except:
        textBox.write("%s port not set correctly." %(ComPort.get()))
        root.update_idletasks()
        comButton.wait_variable(error)
        root.update_idletasks()
    
      
        



# Set SENDING indicator
def SetSendingLight():
    if(textBox.indicator.get() == 0):
        radioSending['state'] = NORMAL
        textBox.indicator.set(1)
        radioSending['fg'] = 'green'

    else:
        textBox.indicator.set(0)
        radioSending['fg'] = 'gray'
        radioSending['state'] = DISABLED


# Function for sending files
def SendDoc():
    SetSendingLight()
    route = filedialog.askopenfilename()
    textBox.write(route)
    try:
        root.after(0, SendMain(ser, route, textBox))
        textBox.write("Sent Successfully.")

    except:
        textBox.write("Something went wrong. Check the file URL")
    SetSendingLight()

# Function for sending a Private Message
def SendMessage():
    SetSendingLight()
    mg = Chatmg.get()
    Chatmg.delete(0, 'end')
    if (len(mg) > 0):
        textBox.write("\n Message: %s" % (mg))
        try:
            root.after(0, SendMg(ser, mg, textBox))
            textBox .write("Sent successfully")
        except:
            textBox.write("Something went wrong.")
    else:
        textBox.write("You must write something.")
    SetSendingLight()


# Class defined for the prompt.
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

    def PB_step(self, step, rst):
        if not rst:
            self.progressbar['value'] += step
        else:
            self.progressbar['value'] = 0
        root.update_idletasks()

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

radioSending = Radiobutton(titleBox, text="Sending", fg="gray",
                           indicatoron=False, state=DISABLED, width=10, value=1)
radioSending.grid(row=0, column=2, sticky="e")
com = Entry(titleBox, width=13,justify=CENTER)
com.grid(row=3,column=2,sticky="e")
com.insert(0,"COM5")

ComPort = StringVar()

comButton = Button(titleBox,width=10,text="Set COM",command=OpenCom)
comButton.grid(row=4,column=2,sticky="e")


optionBox = Frame(root)
optionBox.pack(fill="x")
optionBox.columnconfigure([0, 3], weight=1)

Searchtxt = Entry(optionBox)
Searchtxt.grid(row=1, column=1, pady=5, sticky="ew")

searchBut = Button(optionBox, text="Google Search")
searchBut.grid(row=1, column=2, sticky="ew", pady=5, padx=5)

Chatmg = Entry(optionBox)
Chatmg.grid(row=2, column=1, pady=5, sticky="ew")
Chatmg.config(justify="left", state="normal")
chatBut = Button(optionBox, text="Send Private Message", command=SendMessage)
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
root.wait_variable(error)

textBox.write("%s port set correctly" %(ComPort.get()))
textBox.write("\n LORA NET console. Version 1.0.")
textBox.write("Options available: \n 1) Google Search: Enter a word or sentence to look for. Once the title is choosed, the text in the page will be returned. \n 2) Send Private Message: Fill the box with the message you would like to send privately. \n 3) Send File: Select the file you would like to send.")
textBox.write("Enjoy the radio!")
#Start listening to arduino Serial in parallel thread
threading.Thread(target= ContinuousReader, args=[ser,textBox]).start()  

#root.after(0,ContinuousReader(ser,textBox))

# Init console message




root.mainloop()
