#!/usr/bin/python

#  Driver for the ADAM-5000
#  Made by Bart Garcia  on 23/07/2015

# Imports
# import time
# import sys
# import serial
#
# #Open the Serial port
# sys.stderr = sys.stdout
# ser = serial.Serial(
# 	port='/dev/ttyS0',
# 	baudrate=9600
# )
# # ser.open()
# ser.isOpen()
#
# while 1:
# 	ser.write('$00M\r\n')
# 	# time.sleep(1)
# 	# print ser.readline()
# 	out = ''
# 	# out += ser.read(1)
# 	while ser.inWaiting() > 0:
# 		out += ser.read(1)
# 	if out != '':
# 		print ">>" + out
# 	else :
# 		print 'Nothing'
# 	time.sleep(1)
import sys, os, serial, threading, getopt , time
import termios, sys, os , fcntl
import datetime
#import command library

def acq_display():
    print 'Acquiring    \r',
    for x in range(10000000):
        x=x+1
    print 'Acquiring.   \r',
    for x in range(10000000):
        x=x+1
    print 'Acquiring..  \r',
    for x in range(10000000):
        x=x+1
    print 'Acquiring... \r',

def get_char_keyboard_nonblock():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    c = None

    try:
        c = sys.stdin.read(1)
    except IOError: pass

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c


import ADAM_5000_constants as func

ser = serial.Serial(0)

def timestamp():
    ts= time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('\t %H:%M:%S \n')
    return st


def reader():
    """loop forever and copy serial->console"""
    while 1:
        data = ser.read()
        sys.stdout.write(data)
        sys.stdout.flush()
def write_command(command):
    ser.write("$"+func.ADM_ADD+command+"\r\n")
    # time.sleep(0.1) # Sleep after each write to ensure the answer is ready when we read
    t = float(time.time())
    while t+0.1 > float(time.time()):
        wait="Keepwaiting"
    # print "$"+func.ADM_ADD+command+"\r\n"
def read_command():
	out = ''
	while ser.inWaiting() > 0:
			out += ser.read(1)
	return out
def read_command_clean():
    aux = ''
    out = ''
    while ser.inWaiting() > 0:
        aux = ser.read(1)
        if aux == '+':
            aux = ' '
        if aux == '-':
            aux = ' -'
        else :
            aux = aux
        # print aux
        out += aux
        aux = ''
    # print out
    return out
def ai_configure(slot,input_range, data_format):
    ser.write("$"+func.ADM_ADD+"S"+slot+func.AI_CONF+input_range+data_format+"\r\n")
    # print ("$"+func.ADM_ADD+"S"+slot+func.AI_CONF+input_range+data_format+"\r\n")
    print "Module Configured for Thermocoupler type K with a 60ms Integration time"
    # time.sleep(0.1) # Sleep after each write to ensure the answer is ready when we read
    t = float(time.time())
    while t+0.1 > float(time.time()):
        wait="Keepwaiting"
    read_command() #Just to clear the Acknowledge back


def get_ai_data(slot):
    ser.write("#"+func.ADM_ADD+"S"+slot+"\r\n")
    # time.sleep(0.1)# Extra delay to allow the system to obtain the data and print it out
    t = float(time.time())
    while t+0.1 > float(time.time()):
        wait="Keepwaiting"
    raw = read_command_clean()
    # print raw
    # print len(raw)
    # aux = raw[6:12]
    # print float(aux)
    l =len(raw)
    return raw[1:l-1]


def find_system():
    write_command(func.READ_MODULE_NAME)
    aux = read_command()
    if aux == '':
        print "Error, No module Found"
        return 1
        exit()
    address = aux[1:3]
    module = aux[3:7]
    # print aux
    # print len(aux)
    print "Found ADAM-"+module+" with address "+ address
    return 0

def find_IOType():
    write_command(func.IO_TYPE)
    aux = read_command()
    mod1 = int(aux[3:5])
    mod2 = int(aux[5:7])
    mod3 = int(aux[7:9])
    mod4 = int(aux[9:11])
    print "Modules are : " , mod1, mod2,mod3,mod4
    if mod1 == 18:
        print "Found ThermoCouple Module on Slot 0"
        return 0
    if mod2 == 18:
        print "Found ThermoCouple Module on Slot 1"
        return 1
    if mod3 == 18:
        print "Found ThermoCouple Module on Slot 2"
        return 2
    if mod4 == 18:
        print "Found ThermoCouple Module on Slot 3"
        return 3


print """
---------------------------------------------------------------------------------
                        ADAM-5000 Python controller V1.0
                            Made By Bart Garcia
---------------------------------------------------------------------------------

This controller is implemented for the ThermoCoupler I/O Module on the ADAM-5000

"""

print ">> Searching for the ADAM-5000 System..."
if find_system() != 0 :
    print "Module not found. Finishing the Server"
    sys.exit(0)
print ">> Looking for I/O modules on the System"
TC_Slot_num=find_IOType()
print ">> Configure the ThermoCouple I/O Module"
ai_configure(str(TC_Slot_num),func.TC_K , '80')
print ">> Ready to obtain Data"
try:
	pwm = int(raw_input('Press any key to start acquisition'))
except ValueError:
	print "Not a valid value, please select a value from the range"
print ">> Obtain data"
print ">> Press x to stop the acquisition"
print 'Acquiring...'
ct_header= 'Current Temperature Readings :'
with open ("data.csv", "w") as output:
    while 1:
        raw = get_ai_data(str(TC_Slot_num))
        t = timestamp()
        output.write(raw+t)
        sys.stdout.write('\r' + ct_header + raw + ' ' * 20) # Print the latest temperature readings
        sys.stdout.flush() # important for the printing in one line to work
        # acq_display()
        if get_char_keyboard_nonblock() == 'x':
            break
print ''
print "Finish acquisition, the data is saved onf data.csv in the same repositiry as the server"

output.close()


ser.close()
sys.exit(0)

# fd = sys.stdin.fileno()
# old = termios.tcgetattr(fd)
# new = termios.tcgetattr(fd)
# new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
# new[6][termios.VMIN] = 1
# new[6][termios.VTIME] = 0
# termios.tcsetattr(fd, termios.TCSANOW, new)
# s = ''    # We'll save the characters typed and add them to the pool.


#
# r = threading.Thread(target=reader)
# r.setDaemon(1)
# r.start()
#
#
# while 1 :
# 	x=ser.write("$00M\r\n")
# 	out = ''
# 	while ser.inWaiting() > 0:
# 			out += ser.read(1)
# 	if out != '':
# 			print ">>" + out
# 	time.sleep(1)
# 	x=ser.write("$002\r\n")
# 	out = ''
# 	while ser.inWaiting() > 0:
# 			out += ser.read(1)
# 	if out != '':
# 			print ">>" + out
# 	time.sleep(1)
