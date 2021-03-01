#! /usr/bin/env python3

# Click on DBC file, overwrite or create CSV file, and actively convert signals in the DBC file to a CSV log for easy interpretation. 

import cantools
import can
from select import select
import sys
import re
import csv
from tkinter import Message, Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

signal_list = ['Time']
values_list = ['']
units_list = ['s']
starttime = float(0)
can_device = 'can0'
bus = can.interface.Bus(can_device, bustype='socketcan')

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
dbcfilename = askopenfilename(title = "Select file",filetypes = (("DBC Files","*.dbc"),("all files","*.*"))) 
outputfile = asksaveasfilename(filetypes = (("CSV Files","*.csv"),("all files","*.*")))


with open(outputfile, "w") as logfile:
    
    writecsv = csv.writer(logfile)
    #db = cantools.database.load_file(sys.argv[1])
    db = cantools.database.load_file(dbcfilename)
    i = str(db.messages)
    msg_list = re.findall(r"'(.*?)'", i)

    for items in msg_list:
        test = db.get_message_by_name(items)

        for items2 in range(len(test.signals)):
            signalline = str(test.signals[items2])
            matches=re.findall(r"'(.*?)'",signalline)
            signal_list.append(matches[0])
            units_list.append(matches[2])

    writecsv.writerow(signal_list)
    print(signal_list)
    writecsv.writerow(units_list)
    print(units_list)
    for items3 in range(len(signal_list)) :
        values_list.append('')
    values_list.pop(0)

    while True:
        try:
            msg = bus.recv()

            if starttime == 0:
                starttime = msg.timestamp

            decoded_msg = db.decode_message(msg.arbitration_id, msg.data)
            sig_breakdown = str(decoded_msg).strip("{}").replace("'","").replace(' ','').split(',')

            for items4 in sig_breakdown:
                signame_val = items4.split(':')
                positionalval = signal_list.index(signame_val[0])
                values_list[positionalval] = signame_val[1]

            values_list[0] = (msg.timestamp - starttime)
            writecsv.writerow(values_list)

            items5=0
            while items5<len(values_list):
	            values_list[items5] = ''
	            items5+=1

        except : 
            pass
