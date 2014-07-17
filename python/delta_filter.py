#!/usr/bin/python
import os
##import xively
import subprocess
import time
import datetime
##import requests
#import smbus
import time
import logging
import datetime
import struct
import sys, getopt
import argparse
import re
from datetime import timedelta 
def signed16int(v):
    if v >= 32768:
        v = v - 65536
    return v

def signed8int(v):
    if v >= 128:
        v = v - 256
    return v

def repairLog(inputfile, outputfile, errorfile):

    print "Starting script. "
    myoutputfile = open ( outputfile, 'w')
    myerrorlogfile = open ( errorfile, 'w')
    myinputfile = open(inputfile, "r")
    next(myinputfile)
    prevLine=''
    for line in myinputfile:
        error = False
        input_cells = re.split(r'[,]', line)
        #print error_cells
        if(len(input_cells) >= 10):
            if (prevLine != ''):
                previous_input_cells = re.split(r'[,]', prevLine)
                previous_time=previous_input_cells[1]
               # print datetime.datetime.strptime(previous_time, " %m/%d/%Y %I:%M:%S %p" )
                if (   (datetime.datetime.strptime(previous_time, " %m/%d/%Y %I:%M:%S %p" )+timedelta(hours=1))
                    < datetime.datetime.strptime(input_cells[1], " %m/%d/%Y %I:%M:%S %p" ) ):
                    print "2 hours time buffer at row :"+ input_cells[0]

            if not   ( 0<= float( input_cells[2] )<= 5   ):
                # myerrorlogfile.write('v1='+input_cells[2]+', 0 <= v1 <= 5, '+ line) 
                error=True
            if not ( 0<= float( input_cells[3] )<= 5   ):
                # myerrorlogfile.write('v2='+input_cells[3]+', 0 <= v2 <= 5, '+line) 
                error=True
            if not ( 0<= float( input_cells[4] )<= 5   ):
                # myerrorlogfile.write('v3='+input_cells[4]+', 0 <= v3 <= 5, '+line) 
                error=True
            if not ( 0<= float( input_cells[5] )<= 5   ):
                # myerrorlogfile.write('v4='+input_cells[5]+', 0 <= v4 <= 5, '+line)
                error=True 
            if not ( 0<= float( input_cells[6] )<= 5   ):
                # myerrorlogfile.write('v5='+input_cells[6]+', 0 <= v5 <= 5, '+line) 
                error=True
            if not ( 0<= float( input_cells[7] )<= 5   ):
                # myerrorlogfile.write('v6='+input_cells[7]+', 0 <= v6 <= 5, '+line) 
                error=True
            if not ( 0<= float( input_cells[8] )<= 5   ):
                # myerrorlogfile.write('v7='+input_cells[8]+', 0 <= v7 <= 5, '+line) 
                error=True
            if not ( 0<= float( input_cells[9])<= 5   ):
                # myerrorlogfile.write('v8='+input_cells[9]+', 0 <= v8 <= 5, '+line) 
                error=True
            if not ( -1<= float( input_cells[10] )<= 1   ):
                # myerrorlogfile.write('v1os='+input_cells[10]+', -1 <= v1os <= 1, '+line)
                error=True 
            if not ( 0<= float( input_cells[11] )<= 4   ):
                # myerrorlogfile.write('chg='+input_cells[11] +', 0 <= chg <= 4, '+line) 
                error=True
            if not ( 0<= float( input_cells[12] ) <= 4  ):
                # myerrorlogfile.write('dis='+input_cells[12] +', 0 <= dis <=4, '+line) 
                error=True
            if not ( 0<= float( input_cells[13] )<= 5   ):
                # myerrorlogfile.write('vref_n='+input_cells[13] +', 0 <= Ref- <=5, '+line)
                error=True 
            if not ( 0<= float( input_cells[14] )<= 5   ):
                # myerrorlogfile.write('ref+='+input_cells[14]+', 0 <= Ref+ <=5, '+line) 
                error=True
            if not ( -15<= float( input_cells[15] )<= 15   ):
                # myerrorlogfile.write('Iavg='+input_cells[15] +', -15 <= Iavg <=15, '+line)
                error=True
            if not ( -15<= float( input_cells[16] )<= 15   ):
                # myerrorlogfile.write('Iinst='+input_cells[16] +', -15 <= Iinst <=15, '+line) 
                error=True
            if not ( 0<= float( input_cells[17] )<= 35   ):
                # myerrorlogfile.write('Vtot='+input_cells[17] + ',0 <= Vtot <=35, '+line)
                error=True 
            if not ( 0<= float( input_cells[18] )<= 5   ):
                # myerrorlogfile.write('V1_BG='+input_cells[18]+',0 <= V1_BG <=5, '+line) 
                error=True
            if not ( 0<= float( input_cells[19] )<= 100   ):
                # myerrorlogfile.write('temp='+input_cells[19]+', 0 <= temp <=100, '+line) 
                error=True
            if not ( 0 <= int( input_cells[20] )<= 100   ):
                # myerrorlogfile.write('SOH='+input_cells[20]+', 0 <= SOH <=100, '+line) 
                error=True
            if not ( 0<= int(input_cells[21])<= 32767 ):      
                # myerrorlogfile.write('Cylcnt='+input_cells[21]+', 0 <= cylcnt <=32767 '+line)
                error=True  
            if not ( 0 <= int( input_cells[22] )<= 100   ):
                # myerrorlogfile.write('SOC='+input_cells[22]+', 0 <= SOC <=100, '+line) 
                error=True
            if not ( 0<= float( input_cells[23] )<= 4   ):
                # myerrorlogfile.write('BalB='+input_cells[23]+', 0 <= BalB <=4, '+line)
                error=True 
            if not ( 5<= float( input_cells[24] )<= 8 or float( input_cells[24] )==0   ):
                # myerrorlogfile.write('BalT='+input_cells[24]+', 5 <= BalT <=8 or 0== BalT '+line)
                error=True   
              
            ##    print 'dict string=', battery_dict
            if ( error == False ):
                myoutputfile.write(line)
            else:
                myerrorlogfile.write(line)
        prevLine=line

    myoutputfile.close()
    myinputfile.close()
    myerrorlogfile.close()
    print 'done script'
             
        
inputfile = ''
outputfile = ''
parser = argparse.ArgumentParser(description="repair log", prog="repair")
parser.add_argument('-i', dest='inputfile', action='store', help='inputfile')
parser.add_argument('-o', dest='outputfile', action ='store', help ='outputfile')
parser.add_argument('-e', dest='errorfile', action ='store', help ='errorfile')

args=parser.parse_args()
print(args.inputfile)
print(args.outputfile)
print(args.errorfile)
repairLog(args.inputfile, args.outputfile, args.errorfile)


