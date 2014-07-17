#!/usr/bin/python
import os
##import xively
import subprocess
import time
import datetime
##import requests
import smbus
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

def batterylogging(outputfile):
    i2cAddr=0x28
    datalog =[]
    battery_dict={}
    FEED_ID = '577572561'
    API_KEY = 'yP6mirzrHR6fGiLEeZ26dqOk1EiQUpBDjoV2BKahAJSXqNbY'
    # initialize api client
    ##api = xively.XivelyAPIClient(API_KEY)
    pwd= os.getcwd()+'/'
    logfilename=datetime.datetime.now().strftime(pwd+outputfile+'_%m_%d_%Y_%I_%M_%p.csv')
    logfile=open(logfilename, 'a')
    errorlogfilename=logfilename[:-4]+"_error.csv"
    errorlogfile=open(errorlogfilename, 'a')
    ##  logging.basicConfig(filename=logfile, level=logging.DEBUG)
    ##  print 'Output are being generated to file named: '+ logfile
    ##  print 'where the format of the file name is: battery_data_logfile_%Hour_%Minute_%Day_%Month.log'
    ##  print 'Press Control + C to stop it anytime'
    print "Starting script. Log file is ouput to: "+logfilename + "\n Error file is ouput to:" + errorlogfilename
    ##  feed = api.feeds.get(FEED_ID)
    ####  datastream = get_datastream(feed)
    ##  voltage_1_datastream = feed.datastreams.get("voltage_1")
    ##  voltage_1_datastream.max_value =5 
    ##  voltage_1_datastream.min_value = 3
    ##  voltage_2_datastream = feed.datastreams.get("voltage_2")
    ##  voltage_2_datastream.max_value = 5
    ##  voltage_2_datastream.min_value = 3
    ##  voltage_3_datastream = feed.datastreams.get("voltage_3")
    ##  voltage_3_datastream.max_value = 5
    ##  voltage_3_datastream.min_value = 3
    ##  voltage_4_datastream = feed.datastreams.get("voltage_4")
    ##  voltage_4_datastream.max_value = 5
    ##  voltage_4_datastream.min_value = 3
    ##  voltage_5_datastream = feed.datastreams.get("voltage_5")
    ##  voltage_5_datastream.max_value = 5
    ##  voltage_5_datastream.min_value = 3
    ##  voltage_6_datastream = feed.datastreams.get("voltage_6")
    ##  voltage_6_datastream.max_value = 5
    ##  voltage_6_datastream.min_value = 3
    ##  voltage_7_datastream = feed.datastreams.get("voltage_7")
    ##  voltage_7_datastream.max_value = 5
    ##  voltage_7_datastream.min_value = 3
    ##  temp_datastream = feed.datastreams.get("temp")
    ##  temp_datastream.max_value = 40
    ##  temp_datastream.min_value = 0
    ##  bms_volt_datastream = feed.datastreams.get("bms_volt")
    ##  bms_volt_datastream.max_value = 5
    ##  bms_volt_datastream.min_value = 3
    ##  current_datastream = feed.datastreams.get("current")
    ##  current_datastream.max_value = 5
    ##  current_datastream.min_value = 3
    ##  instant_current_datastream = feed.datastreams.get("instant_current")
    ##  instant_current_datastream.max_value = 5
    ##  instant_current_datastream.min_value = 3
    ##  tick_datastream = feed.datastreams.get("tick")
    ##  state_of_charge_datastream = feed.datastreams.get("state_of_charge")
    ##  state_of_charge_datastream.max_value = 100
    ##  state_of_charge_datastream.min_value = 0
    ##  state_of_health_datastream = feed.datastreams.get("state_of_health")
    ##  state_of_health_datastream.max_value = 100
    ##  state_of_health_datastream.min_value = 0
      
    bus = smbus.SMBus(1)
    tcnt=0
    logfile.write('Tcnt,Time,V1,V2,V3,V4,V5,V6,V7,V8,V1os,chg,disch,Ref-,Ref+,Iavg,Iinst,Vtot,V1_BG,Temp,SOH,Cylcnt,SOC,BalB,BalT,Addr,Tic,dTic\n')
    while True:
        tcnt=tcnt+1
        i2cdata = []
        error=False
        for a in range(0,63):
            x = bus.read_byte_data(0x28,a)
            i2cdata.append(x)               
        state_of_health_flag = int(i2cdata[51])
        SOH='0'
        if state_of_health_flag == 3:
            SOH = str(i2cdata[50])
        voltage_1="%.3f"%((i2cdata[2]|((i2cdata[3]&0xff)<<8))/1000.0)
        voltage_2="%.3f"%((i2cdata[4]|((i2cdata[5]&0xff)<<8))/1000.0)
        voltage_3="%.3f"%((i2cdata[6]|((i2cdata[7]&0xff)<<8))/1000.0)
        voltage_4="%.3f"%((i2cdata[8]|((i2cdata[9]&0xff)<<8))/1000.0)
        voltage_5="%.3f"%((i2cdata[10]|((i2cdata[11]&0xff)<<8))/1000.0)
        voltage_6="%.3f"%((i2cdata[12]|((i2cdata[13]&0xff)<<8))/1000.0)
        voltage_7="%.3f"%((i2cdata[14]|((i2cdata[15]&0xff)<<8))/1000.0)
        voltage_8="%.3f"%((i2cdata[16]|((i2cdata[17]&0xff)<<8))/1000.0)
        temp="%.3f"%((signed16int(i2cdata[26]|((i2cdata[27]&0xff)<<8))-2731.5)/10)
        Cylcnt= str((i2cdata[52]  | ((i2cdata[53] & 0xFF) << 8)))
        V1_BG="%.3f"%((i2cdata[28]|((i2cdata[29]&0xff)<<8))/1000.0)
        Iavg="%.3f"%((signed16int(i2cdata[30]|((i2cdata[31]&0xff)<<8))/1000.0))
        Iinst="%.3f"%((signed16int(i2cdata[40]|((i2cdata[41]&0xff)<<8))/1000.0))
        tick=str((i2cdata[46]|((i2cdata[47]&0xff)<<8)|((i2cdata[48]&0xff)<<16)|((i2cdata[49]&0xff)<<24)))
        SOC=str((i2cdata[54]|((i2cdata[55]&0xff)<<8)))
        BalT=str(i2cdata[56])
        BalB=str(i2cdata[57])
        chg = "%.3f"%(i2cdata[20])
        dis = "%.3f"%(i2cdata[21])
        Vtot="%.3f"%(float(voltage_1) + float(voltage_2)+ float(voltage_3)+float(voltage_4)+float(voltage_5)+float(voltage_6)+float(voltage_7)+float(voltage_8))
        vref_n= "%.3f"%((i2cdata[22]  | ((i2cdata[23] & 0xFF) << 8))/1000.0)
        vref_p="%.3f"%((i2cdata[24]  | ((i2cdata[25] & 0xFF) << 8))/1000.0)
        v1os="%.3f"%((signed16int(i2cdata[18]|((i2cdata[19]&0xff)<<8))/1000.0))
        jumper= str( hex(i2cAddr*2) )
        timelog = datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        debugstring= (str(tcnt)+', '+str(timelog)+', '+voltage_1+', '+voltage_2+', '+voltage_3+', '+voltage_4+', '+voltage_5+', '+
                          voltage_6+', '+voltage_7+', '+voltage_8+', '+v1os+', '+chg+', '+dis+', '+vref_n+', '+vref_p+', '+
                          Iavg+', '+Iinst+', '+Vtot+', '+V1_BG+', '+temp+', '+SOH+', '+Cylcnt+', '+
                          SOC+', '+BalB+', '+BalT+', '+jumper+', '+tick+', '+'1')
        if not   ( 0<= float( voltage_1 )<= 5   ):
            # errorlogfile.write('v1='+voltage_1+', 0 <= v1 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_2 )<= 5   ):
            # errorlogfile.write('v2='+voltage_2+', 0 <= v2 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_3 )<= 5   ):
            # errorlogfile.write('v3='+voltage_3+', 0 <= v3 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_4 )<= 5   ):
            # errorlogfile.write('v4='+voltage_4+', 0 <= v4 <= 5, '+str(tcnt)+' ,'+debugstring)
            error=True 
        if not ( 0<= float( voltage_5 )<= 5   ):
            # errorlogfile.write('v5='+voltage_5+', 0 <= v5 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_6 )<= 5   ):
            # errorlogfile.write('v6='+voltage_6+', 0 <= v6 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_7 )<= 5   ):
            # errorlogfile.write('v7='+voltage_7+', 0 <= v7 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( voltage_8)<= 5   ):
            # errorlogfile.write('v8='+voltage_8+', 0 <= v8 <= 5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( -1<= float( v1os )<= 1   ):
            # errorlogfile.write('v1os='+v1os+', -1 <= v1os <= 1, '+str(tcnt)+' ,'+debugstring)
            error=True 
        if not ( 0<= float( chg )<= 4   ):
            # errorlogfile.write('chg='+chg+', 0 <= chg <= 4, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( dis ) <= 4  ):
            # errorlogfile.write('dis='+dis+', 0 <= dis <=4, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( vref_n )<= 5   ):
            # errorlogfile.write('vref_n='+vref_n+', 0 <= Ref- <=5, '+str(tcnt)+' ,'+debugstring)
            error=True 
        if not ( 0<= float( vref_p )<= 5   ):
            # errorlogfile.write('ref+='+vref_p+', 0 <= Ref+ <=5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( -15<= float( Iavg )<= 15   ):
            # errorlogfile.write('Iavg='+Iavg+', -15 <= Iavg <=15, '+str(tcnt)+' ,'+debugstring)
            error=True
        if not ( -15<= float( Iinst )<= 15   ):
            # errorlogfile.write('Iinst='+Iinst+', -15 <= Iinst <=15, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( Vtot )<= 35   ):
            # errorlogfile.write('Vtot='+Vtot+ ',0 <= Vtot <=35, '+str(tcnt)+' ,'+debugstring)
            error=True 
        if not ( 0<= float( V1_BG )<= 5   ):
            # errorlogfile.write('V1_BG='+V1_BG+',0 <= V1_BG <=5, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( temp )<= 100   ):
            # errorlogfile.write('temp='+temp+', 0 <= temp <=100, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0 <= int( SOH )<= 100   ):
            # errorlogfile.write('SOH='+SOH+', 0 <= SOH <=100, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0 <= int( SOC )<= 100   ):
            # errorlogfile.write('SOC='+SOC+', 0 <= SOC <=100, '+str(tcnt)+' ,'+debugstring) 
            error=True
        if not ( 0<= float( BalB )<= 4   ):
            # errorlogfile.write('BalB='+BalB+', 0 <= BalB <=4, '+str(tcnt)+' ,'+debugstring)
            error=True 
        if not ( 5<= float( BalT )<= 8 or float( BalT )==0   ):
            # errorlogfile.write('BalT='+BalT+', 5 <= BalT <=8 or 0== BalT '+str(tcnt)+' ,'+debugstring)
            error=True   
        if not ( 0<= int(Cylcnt)<= 32767 ):      
            # errorlogfile.write('Cylcnt='+Cyclnt+', 0 <= cylcnt <=32767 '+str(tcnt)+' ,'+debugstring)
            error=True                
        print debugstring
        ##    print 'dict string=', battery_dict
        if ( error == False ):
            logfile.write(debugstring+'\n')
        else:
            errorlogfile.write(debugstring+'\n')

        time.sleep(0.95)
        ##    voltage_1_datastream.current_value = voltage_1
        ##    voltage_1_datastream.at = datetime.datetime.utcnow()
        ##    voltage_2_datastream.current_value = voltage_2
        ##    voltage_2_datastream.at = datetime.datetime.utcnow()
        ##    voltage_3_datastream.current_value = voltage_3
        ##    voltage_3_datastream.at = datetime.datetime.utcnow()
        ##    voltage_4_datastream.current_value = voltage_4
        ##    voltage_4_datastream.at = datetime.datetime.utcnow()
        ##    voltage_5_datastream.current_value = voltage_5
        ##    voltage_5_datastream.at = datetime.datetime.utcnow()
        ##    voltage_6_datastream.current_value = voltage_6
        ##    voltage_6_datastream.at = datetime.datetime.utcnow()
        ##    voltage_7_datastream.current_value = voltage_7
        ##    voltage_7_datastream.at = datetime.datetime.utcnow()
        ##    temp_datastream.current_value = temp
        ##    temp_datastream.at = datetime.datetime.utcnow()
        ##    bms_volt_datastream.current_value = bms_volt
        ##    bms_volt_datastream.at = datetime.datetime.utcnow()
        ##    current_datastream.current_value = current
        ##    current_datastream.at = datetime.datetime.utcnow()
        ##    instant_current_datastream.current_value = instant_current
        ##    instant_current_datastream.at = datetime.datetime.utcnow()
        ##    tick_datastream.current_value = tick
        ##    tick_datastream.at = datetime.datetime.utcnow()
        ##    state_of_charge_datastream.current_value = state_of_charge
        ##    state_of_charge_datastream.at = datetime.datetime.utcnow()
        ##    state_of_health_datastream.current_value = state_of_health
        ##    state_of_health_datastream.at = datetime.datetime.utcnow()
            
        ##    try:
        ####      voltage_1_datastream.update()
        ####      voltage_2_datastream.update()
        ####      voltage_3_datastream.update()
        ####      voltage_4_datastream.update()
        ####      voltage_5_datastream.update()
        ####      voltage_6_datastream.update()
        ####      voltage_7_datastream.update()
        ####      bms_volt_datastream.update()
        ####      current_datastream.update()
        ####      instant_current_datastream.update()
        ####      tick_datastream.update()
        ####      state_of_charge_datastream.update()
        ####      state_of_health_datastream.update()
        ####      temp_datastream.update()
        ####
        ####      
        ####    except requests.HTTPError as e:
        ####      print 'something wrong!', e
        ####      logging.debug(e)
        ####      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
                  
               
               
        ##def batteryTickLogging():
        ##  logfile = datetime.datetime.now().strftime('battery_data_logfile_%H_%M_%d_%m.log')
        ##  logging.basicConfig(filename=logfile, level=logging.DEBUG)
        ##  print 'Output are being generated to file named: '+ logfile
        ##  print 'where the format of the file name is: battery_data_logfile_%Hour_%Minute_%Day_%Month.log'
        ##  print 'Press Control + C to stop it anytime'
        ##  bus = smbus.SMBus(1)
        ##  for b in range(0,100):
        ##      i2cdata = []
        ##      for a in range(0,63):
        ##          i2cdata.append(bus.read_byte_data(0x28,a))
        ##      for a in range(2,21,2):
        ##            volt1= str((i2cdata[a]|((i2cdata[a+1]&0xff)<<8))/1000.0)
        ##          debugstring= str((i2cdata[a]|((i2cdata[a+1]&0xff)<<8))/1000.0)+','+str((signed16int(i2cdata[26]|((i2cdata[27]&0xff)<<8))-2731.5)/10)+','+str(signed16int(i2cdata[28]|((i2cdata[29]&0xff)<<8))/1000.0)+','+str(signed16int(i2cdata[30]|((i2cdata[31]&0xff)<<8))/1000.0)+','+str(signed16int(i2cdata[40]|((i2cdata[41]&0xff)<<8))/1000.0)+','+ str((i2cdata[46]|((i2cdata[47]&0xff)<<8)|((i2cdata[48]&0xff)<<16)|((i2cdata[49]&0xff)<<24)))+','+ str((i2cdata[54]|((i2cdata[55]&0xff)<<8)))
        ##          logging.debug(debugstring)
        ##          time.sleep(.95)
        ##          print 'batteryTickLogging()=', str((i2cdata[46]|((i2cdata[47]&0xff)<<8)|((i2cdata[48]&0xff)<<16)|((i2cdata[49]&0xff)<<24)))
        ##          return str((i2cdata[46]|((i2cdata[47]&0xff)<<8)|((i2cdata[48]&0xff)<<16)|((i2cdata[49]&0xff)<<24)))
        ##            
        ### extract feed_id and api_key from environment variables
        #FEED_ID = os.environ["FEED_ID"]
        #API_KEY = os.environ["API_KEY"]


        # function to read 1 minute load average from system uptime command
        ##def read_loadavg():
        ##  if DEBUG:
        ##    print "Reading load average"
        ##  # return subprocess.check_output(["awk '{print $1}' /proc/loadavg"], shell=True)
        ##  return batteryLogging()

        ### function to read 1 minute load average from system uptime command
        ##def read_batterytick():
        ##  if DEBUG:
        ##    print "Reading load average"
        ##  # return subprocess.check_output(["awk '{print $1}' /proc/loadavg"], shell=True)
        ##  return batteryTickLogging()

        ##def read_batteryLog_Dict():
        ##  if DEBUG:
        ##    print "Reading load average"
        ##  # return subprocess.check_output(["awk '{print $1}' /proc/loadavg"], shell=True)
        ##  return batteryLogging()
        ##
        ### function to return a datastream object. This either creates a new datastream,
        ### or returns an existing one
        ##def get_datastream(feed):
        ##  try:
        ##    datastream = feed.datastreams.get("voltage_1")
        ##    if DEBUG:
        ##      print "Found existing datastream"
        ##    return datastream
        ##  except:
        ##    if DEBUG:
        ##      print "Creating new datastream"
        ##    datastream = feed.datastreams.create("load_avg", tags="load_01")
        ##    return datastream

        # function to return a datastream object. This either creates a new datastream,
        # or returns an existing one
        ##def get_tick_datastream(feed):
        ##  try:
        ##    datastream = feed.datastreams.get("tick")
        ##    if DEBUG:
        ##      print "Found existing tick datastream"
        ##    return datastream
        ##  except:
        ##    if DEBUG:
        ##      print "Creating new tick datastream"
        ##    datastream = feed.datastreams.create("tick", tags="tick_01")
        ##    return datastream

        # main program entry point - runs continuously updating our datastream with the
        # current 1 minute load average
        ##def run():
        ##  print "Starting Xively tutorial script"
        ##
        ##  feed = api.feeds.get(FEED_ID)
        ####  datastream = get_datastream(feed)
        ##  voltage_1_datastream = feed.datastreams.get("voltage_1")
        ##  voltage_1_datastream.max_value = None
        ##  voltage_1_datastream.min_value = None
        ##  temp_datastream = feed.datastreams.get("temp")
        ##  temp_datastream.max_value = None
        ##  temp_datastream.min_value = None
        ####  tick_datastream = get_tick_datastream(feed)
        ####  tick_datastream.max_value = None
        ####  tick_datastream.min_value = None
        ##
        ##  while True:
        ####    load_avg = read_loadavg()
        ##    batterydict = read_batteryLog_Dict()
        ##    print 'battery dict voltage 1=', batterydict['voltage_1']
        ####    print 'batterytick=', batterytick
        ##    if DEBUG:
        ##      print "Updating Xively feed with value: %s" % batterydict['voltage_1']
        ##
        ##    voltage_1_datastream.current_value = batterydict['voltage_1']
        ##    voltage_1_datastream.at = datetime.datetime.utcnow()
        ##    temp_datastream.current_value = batterydict['temp']
        ##    temp_datastream.at = datetime.datetime.utcnow()
        ##    try:
        ##      voltage_1_datastream.update()
        ##      temp_datastream.update()
        ##    except requests.HTTPError as e:
        ##      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        ##      print 'something wrong and breaking out now'
        ##      break
        ##
        ####    tick_datastream.current_value = batterytick
        ####    tick_datastream.at = datetime.datetime.utcnow()
        ####    try:
        ####      tick_datastream.update()
        ####    except requests.HTTPError as e:
        ####      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        ##
        ##    time.sleep(10)




parser = argparse.ArgumentParser(description="This program will produce a battery log output file", prog="batterylog")
parser.add_argument('-i', dest='inputfile', action='store', help='inputfile')
parser.add_argument('-o', dest='outputfile', action ='store', help ='outputfile')
args=parser.parse_args()
batterylogging(args.outputfile)
