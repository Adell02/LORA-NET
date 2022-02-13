import threading
from tkinter import filedialog
from tkinter.ttk import Progressbar
import webbrowser
import PIL.Image
import PIL.ImageTk
import serial
from tkinter import *
from FileExporterOne import SendFile
from Message import SendMg
from ReceiveReader import ContinuousReader

import config



# Menubar functions
def SavePrompt():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    text2save = str(textBox.textBox.get(1.0,END))
    f.write(text2save)
    f.close()

def selectall():
    textBox.textBox.focus()
    textBox.textBox.tag_add('sel', '1.0', 'end')

def clearall():
    textBox.textBox.config(state=NORMAL)
    textBox.textBox.delete('1.0',END)
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
                "%s port has already been successfully configured" % (ComPort.get()))
        else:
            ser = serial.Serial(port=ComPort.get(), baudrate = config.BAUDRATE, timeout=.1)
            error.set(0)
    except:
        textBox.write("%s port not set correctly." % (ComPort.get()))
        root.update_idletasks()
        comButton.wait_variable(error)
        root.update_idletasks()


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


# Function for sending files
def SendDoc():
    SetSendingLight()
    route = filedialog.askopenfilename()
    textBox.write(route)
    try:
        root.after(0, SendFile(ser, route, textBox))        # Function with the file sending procedure without blocking the interface (thanks to root.after)
        textBox.write("Sent Successfully.")

    except:
        textBox.write("Sending file CANCELLED")
    SetSendingLight()

# Function for sending a Private Message
def SendMessage(event):
    SetSendingLight()
    mg = Chatmg.get()
    Chatmg.delete(0, 'end')     # Erase the entry
    if (len(mg) > 0):
        textBox.write("\n Message: %s" % (mg))
        try:
            root.after(0, SendMg(ser, mg, textBox))     # Fucntion with the message sending procedure
            textBox .write("Sent successfully")
        except:
            textBox.write("Something went wrong.")
    else:
        textBox.write("You must write something.")
    SetSendingLight()


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
filemenu.add_command(label="Save",command=SavePrompt)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear",command=clearall)
editmenu.add_command(label="Select All",command=selectall)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help",command=Help)
helpmenu.add_separator()
helpmenu.add_command(label="About Lora Net",command=AboutLora)

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

radioSending = Radiobutton(titleBox, text="Sending", fg="gray",
                           indicatoron=False, state=DISABLED, width=10, value=1)
radioSending.grid(row=0, column=2, sticky="e")
com = Entry(titleBox, width=13, justify=CENTER)
com.grid(row=3, column=2, sticky="e")
com.insert(0, config.DEFAULT_PORT)
com.bind('<Return>',OpenCom)

ComPort = StringVar()

comButton = Button(titleBox, width=10, text="Set COM", command= lambda: OpenCom(True))
comButton.grid(row=4, column=2, sticky="e")


optionBox = Frame(root)
optionBox.pack(fill="x")
optionBox.columnconfigure([0, 3], weight=1)

Searchtxt = Entry(optionBox)
Searchtxt.grid(row=1, column=1, pady=5, sticky="ew")
#Searchtxt.bind('<Return>',)
searchBut = Button(optionBox, text="Google Search")
searchBut.grid(row=1, column=2, sticky="ew", pady=5, padx=5)

Chatmg = Entry(optionBox)
Chatmg.grid(row=2, column=1, pady=5, sticky="ew")
Chatmg.config(justify="left", state="normal")
Chatmg.bind('<Return>',SendMessage)
chatBut = Button(optionBox, text="Send Private Message", command= lambda: SendMessage(True))
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
textBox.write("Please set the COM port to start using LORA net.")
root.wait_variable(error)

textBox.write("%s port set correctly" % (ComPort.get()))
textBox.write(config.LOG)

# Start listening to arduino Serial in parallel thread
threading.Thread(target=ContinuousReader, args=[ser, textBox]).start()

# Destroy main window when closing app
root.protocol("WM_DELETE_WINDOW", root.destroy)

root.mainloop()
