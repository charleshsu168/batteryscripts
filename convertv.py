import time
from datetime import datetime
import numpy as np
from pylab import figure, show
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import logging
import re 
import string as st
from datetime import timedelta
import Tkinter
import tkMessageBox
import tkMessageBox
from Tkinter import Tk
from tkFileDialog import askopenfilename
from matplotlib.font_manager import FontProperties
import sys, getopt
import argparse
import re
from Tkinter import *
import time

parser = argparse.ArgumentParser(description="""
	This program will accept a battery 
 log input file and convert its time column in the format of 07/08/2014 06:15:29 PM(%m/%d/%Y %I:%M:%S %p) 
 to a Veusz-compatible format 2014-07-08T18:15:27(%Y-%m-%dT%H:%M:%S)""")
parser.add_argument('-i', dest='inputfile', action='store', help='inputfile')
parser.add_argument('-o', dest='outputfile', action ='store', help ='outputfile')
args=parser.parse_args()

try:
	inputfile=open(args.inputfile, 'r' ) #Open files
	outputfile=open(args.outputfile, 'w' )
except Exception, e:
	print "\n\nUse -h for more help\n\n"
	print e
next(inputfile)
for line in inputfile:  # Go through file line one by one in for loop
   input_cells=re.split(r'[;,]', line)
   current_time=datetime.strptime(input_cells[1], " %m/%d/%Y %I:%M:%S %p" ) 
   # unixtime=time.mktime(datetime.strptime(input_cells[1], " %m/%d/%Y %I:%M:%S %p" ).timetuple())
   # "2013-12-22T21:08:07"
   input_cells[1]=datetime.strftime(current_time, "%Y-%m-%dT%H:%M:%S" )
   # print 'unix time=', unixtime
   # input_cells[1]=str(unixtime)[:-2]
   outputfile.write(','.join(input_cells))
inputfile.close()
outputfile.close()



