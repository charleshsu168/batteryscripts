batteryscripts
==============
batterylog is a python script to log live RPI battery pack data:


To use it
==============
sudo python batterylog.py -o outfilename


Output
==============
Tcnt,Time,V1,V2,V3,V4,V5,V6,V7,V8,V1os,chg,disch,Ref-,Ref+,Iavg,Iinst,Vtot,V1_BG,Temp,SOH,Cylcnt,SOC,BalB,BalT,Addr,Tic,dTic
1, 07/08/2014 06:15:27 PM, 4.043, 4.045, 4.055, 4.090, 4.087, 4.091, 4.078, 4.116, -0.281, 0.000, 2.000, 3.033, 4.429, -12.787, -12.782, 32.605, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635197, 1
2, 07/08/2014 06:15:28 PM, 4.042, 4.044, 4.056, 4.090, 4.086, 4.093, 4.077, 4.121, -0.280, 0.000, 2.000, 3.033, 4.429, -12.786, -12.782, 32.609, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635198, 1
3, 07/08/2014 06:15:29 PM, 4.042, 4.043, 4.054, 4.090, 4.086, 4.093, 4.077, 4.123, -0.280, 0.000, 2.000, 3.033, 4.429, -12.789, -12.785, 32.608, 4.036, 26.350, 0, 0, 92, 0, 0, 0x50, 1635199, 1
...........
...........


xbatterylog 
==============
is a python script to upload live RPI battery pack to xively.com


To use it
==============
sudo python xbatterylog.py 

Output
==============
it output data to xively.com public feed.
To view it go to feed: https://xively.com/feeds/577572561
or download an Android app, xively viewer, to view the data on an Android tablet.



