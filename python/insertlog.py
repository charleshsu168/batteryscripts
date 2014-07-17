#!/usr/bin/python
import os
##import xively
import subprocess
import time
import datetime
##import requests
# import smbus
import time
import logging
import datetime
import struct
import sys, getopt
import argparse
import re
def signed16int(v):
    if v >= 32768:
        v = v - 65536
    return v

def signed8int(v):
    if v >= 128:
        v = v - 256
    return v

def insertLog(args_inputfile, args_outputfile, args_errorfile):

    print "Starting script. "

    inputfile = open(args_inputfile, 'r')
    outputfile = open ( args_outputfile, 'w')
    errorfile=open( args_errorfile, 'r')
    filecontents = inputfile.readlines()
    for line in errorfile:
        if line.isspace():
            pass
        else:
            input_cells = re.split(r'[,]', line)
            filecontents.insert(int(input_cells[0].strip()), line)
    filecontents = "".join(filecontents)
    outputfile.write(filecontents)
    inputfile.close()
    outputfile.close()
    errorfile.close()
             
        

parser = argparse.ArgumentParser(description="repair log", prog="repair")
parser.add_argument('-i', dest='inputfile', action='store', help='inputfile')
parser.add_argument('-o', dest='outputfile', action ='store', help ='outputfile')
parser.add_argument('-e', dest='errorfile', action ='store', help ='errorfile')

args=parser.parse_args()
print(args.inputfile)
print(args.outputfile)
print(args.errorfile)
insertLog(args.inputfile, args.outputfile, args.errorfile)


