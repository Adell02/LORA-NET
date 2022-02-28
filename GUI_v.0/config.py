# Config file. Constants and Settings

LOG = "\n LORA NET . Version 1.0.\n Options available: \n 1) Google Search: Enter a word or sentence to look for. Once the title is choosed, the text in the page will be returned. \n 2) Send Private Message: Fill the box with the message you would like to send privately. \n 3) Send File: Select the file you would like to send.\n Enjoy the radio!"
ID = 1
ALL_ID = 0
BAUDRATE = 9600
DEFAULT_PORT = "COM4"

ID_MARKER = "#"
FROM_TO_MARKER = ":"
END_MARKER = "*"

FILE_SPLIT = 255 - len(ID_MARKER) - len(FROM_TO_MARKER) - len(END_MARKER) - len(str(ID))       # MAX bytes = 255. Character = 4 bytes (encoded) with some margin for header and markers
MG_SPLIT = 255 - len(ID_MARKER) - len(FROM_TO_MARKER) - len(END_MARKER) - len(str(ID))
PCKT_SLEEP = 1.5    # TIME RESTING AFTER SENDING A PACKET


IN_FILE_URL = 'received_file.rar'
IN_SEARCH_URL = "received_results_GS.zip"
