BATTERY SCRIPTS
==============
This is a collection of python scripts useful for lab batttery testing. 

BATTERYLOG.PY
==============
batterylog is a python script for RPI  to stream realtime battery pack data to screen and to outputfile as specified by user.

It will filter out abnormal ranges of values and outputs it to  outpfile_error.csv

It currently does not support running Cygwin in Windows via USB to battery pack.

TO INSTALL IT
==============
 Download the scripts and unzip it to a folder. 
 Connect all the wires to RPI and the battery packs as in the lab environment. 
 Run the script.

TO USE IT
==============

sudo python batterylog.py -o outputfilename.csv

usage: batterylog [-h] [-o OUTPUTFILE]

This program will produce a battery log output file and an error log file.

required arguments:
  -o outputfile

optional arguments:
  -h, --help     show this help message and exit


OUTPUT
==============
Tcnt,Time,V1,V2,V3,V4,V5,V6,V7,V8,V1os,chg,disch,Ref-,Ref+,Iavg,Iinst,Vtot,V1_BG,Temp,SOH,Cylcnt,SOC,BalB,BalT,Addr,Tic,dTic 

1, 07/08/2014 06:15:27 PM, 4.043, 4.045, 4.055, 4.090, 4.087, 4.091, 4.078, 4.116, -0.281, 0.000, 2.000, 3.033, 4.429, -12.787, -12.782, 32.605, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635197, 1

2, 07/08/2014 06:15:28 PM, 4.042, 4.044, 4.056, 4.090, 4.086, 4.093, 4.077, 4.121, -0.280, 0.000, 2.000, 3.033, 4.429, -12.786, -12.782, 32.609, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635198, 1

3, 07/08/2014 06:15:29 PM, 4.042, 4.043, 4.054, 4.090, 4.086, 4.093, 4.077, 4.123, -0.280, 0.000, 2.000, 3.033, 4.429, -12.789, -12.785, 32.608, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635199, 1

...........
...........

to an outputfile

XBATTERYLOG.PY
==============
is a python script to upload live RPI's battery pack data to xively.com


TO USE IT
==============
sudo python xbatterylog.py 


OUTPUT
==============
it upload data to xively cloud every minute( SOC, dis, chg, temp). To view the live data while the battery is dishcharging/charing and running the script, go to feed: https://xively.com/feeds/577572561
or download an Android app, xively viewer, to view the data on an Android tablet.
FEED_ID = '577572561'

CONVERTV.PY
==============
is a python script to convert log file's time column  to a different time format for viewing in Veusz:

07/08/2014 06:15:29 PM converts to 2014-07-08T18:15:27


In other words, it converts time in the format of %m/%d/%Y %I:%M:%S %p  to %Y-%m-%dT%H:%M:%S

in order to display x-axis as date and time Veusz.


TO USE IT
==============
sudo python convertv.py -i inputfilename -o outputfilename

