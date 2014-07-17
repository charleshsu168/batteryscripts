#! /usr/bin/awk -f

#  pgm_date = " Thu, Jul 10, 2014  4:36:19 PM "
#  change from fUSBcsv.awk for RPI log file filtering
#  watch for the first field & 1st header title line

#  pgm_date = " Thu, Jul 10, 2014  4:02:03 PM "
#  field parameterized
#  change default VxMin=2, VtotMin=16  instead of 0,0 for both case


#  pgm_date = " Tue, Jul 08, 2014  2:01:52 PM "
#  to fix Tic number too big, so the Cylcnt = 117 can be eliminated
#  to check if Tic increment is bigger than 10, then prtoaky = 0
#  TicDIFF = 1000  this number will change, if two csv is merged, then TicDIFF can be big

#  pgm_date = " Mon Jul  7 18:12:59 PDT 2014 "
#  NR, Tcnt twice

#  pgm_date = " Mon Jul  7 14:43:42 PDT 2014 "
#  the stderr doesn't work, so it is change to >C_

#  pgm_date = " Mon, Jul 07, 2014  1:51:19 PM "
#  pgm_date = " Mon, Jul 07, 2014 10:54:49 AM " begin

#  gsub( /^ *| *$/, "", item )  doesn't work
BEGIN {
## for USB case
#  Ticfld = 26
#  V1fld = 2
#  V1osfld = 10
#  chgfld = 11
#  Ref_fld = 13
# for RPI case
  Ticfld = 27
  V1fld = 3
  V1osfld = 11
  chgfld = 12
  Ref_fld = 14

#USB csv         1    2  3  4  5  6  7  8  9  10   11  12    13   14   15   16    17   18    19   20  21     22  23   24   25   26
#           1    2    3  4  5  6  7  8  9  10 11   12  13    14   15   16   17    18   19    20   21  22     23  24   25   26   27  28
  header = "Tcnt,Time,V1,V2,V3,V4,V5,V6,V7,V8,V1os,chg,disch,Ref-,Ref+,Iavg,Iinst,Vtot,V1_BG,Temp,SOH,Cylcnt,SOC,BalB,BalT,Addr,Tic,dTic"
  pgm_date = " Thu, Jul 10, 2014  4:36:19 PM "
  awkpgm = "fRPIcsv.awk"
  rev = "Rev 0.0"
#    ( BVmin == "" ) ? Vbg = 3 : Vbg = BVmin
  ( VxMin == "" ) ? VxMIN = 2 : VxMIN = VxMin
#  ( VxMin == "" ) ? VxMIN = 0 : VxMIN = VxMin
  ( VxMax == "" ) ? VxMAX = 5 : VxMAX = VxMax
#  ( VtotMin == "" ) ? VtotMIN = 0 : VtotMIN = VtotMin
  ( VtotMin == "" ) ? VtotMIN = 16 : VtotMIN = VtotMin
  ( VtotMax == "" ) ? VtotMAX = 35 : VtotMAX = VtotMax
  ( V1osMin == "" ) ? V1osMIN = -1 : V1osMIN = V1osMin
  ( V1osMax == "" ) ? V1osMAX = 1 : V1osMAX = V1osMax
  ( chgMin == "" ) ? chgMIN = 0 : chgMIN = chgMin
  ( chgMax == "" ) ? chgMAX = 4 : chgMAX = chgMax
  ( dischMin == "" ) ? dischMIN = 0 : dischMIN = dischMin
  ( dischMax == "" ) ? dischMAX = 4 : dischMAX = dischMax
  ( IavgMin == "" ) ? IavgMIN = -15 : IavgMIN = IavgMin
  ( IavgMax == "" ) ? IavgMAX = 15 : IavgMAX = IavgMax
  ( IinstMin == "" ) ? IinstMIN = -15 : IinstMIN = IinstMin
  ( IinstMax == "" ) ? IinstMAX = 15 : IinstMAX = IinstMax
  ( TempMin == "" ) ? TempMIN = 0 : TempMIN = TempMin
  ( TempMax == "" ) ? TempMAX = 100 : TempMAX = TempMax
  ( SOCMin == "" ) ? SOCMIN = 0 : SOCMIN = SOCMin
  ( SOCMax == "" ) ? SOCMAX = 100 : SOCMAX = SOCMax
  ( SOHMin == "" ) ? SOHMIN = 0 : SOHMIN = SOHMin
  ( SOHMax == "" ) ? SOHMAX = 100 : SOHMAX = SOHMax
  ( CylcntMin == "" ) ? CylcntMIN = 0 : CylcntMIN = CylcntMin
  ( CylcntMax == "" ) ? CylcntMAX = 32767 : CylcntMAX = CylcntMax
  ( BalBMin == "" ) ? BalBMIN = 1 : BalBMIN = BalBMin
  ( BalBMax == "" ) ? BalBMAX = 4 : BalBMAX = BalBMax
  ( BalTMin == "" ) ? BalTMIN = 5 : BalTMIN = BalTMin
  ( BalTMax == "" ) ? BalTMAX = 8 : BalTMAX = BalTMax
  ( BalTMax == "" ) ? BalTMAX = 8 : BalTMAX = BalTMax
  ( TicDiff == "" ) ? TicDIFF = 1000 : TicDIFF = TicDiff

  if ( ARGV[1] == "" ) {
#    system( "clear" )
    printf( "\n     To filter out abnormal item from RPI csv file\n" )
    printf( "\n" )
    printf( "Usage: %s anyRPIcsv.csv                          anyRPIcsv.csv csv file from I2C to RPI interface\n", awkpgm )
    printf( "          C_anyRPIcsv.csv         consecutive Tcnt file can be Veusz-ed, after abnormal lines are thrown away\n" )
    printf( "          V_anyRPIcsv_error.csv   abnormal lines are captured in this Veusz-able csv file, so correctness can be examined graphically\n" )
    printf( "          tmp_anyRPIcsv.csv.error  tmp_anyRPIcsv.csv  pairs can be used to constuct back shouldn't thrown away lines (if some mistakes bave been made)\n" )
    printf( "\n" )
    printf( "          Default values used,  note that VxMin=%d, VtotMin=%d\n", VxMIN, VtotMIN )
    printf( "          V1-V8, Ref-, Ref+, V1_BG:  VxMin:%s VxMax:%s\n", VxMIN, VxMAX )
    printf( "          V1os                    :  V1osMin:%s V1osMax:%s\n", V1osMIN, V1osMAX )
    printf( "          chg, disch              :  chMin:%s chMax:%s\n", chgMIN, chgMAX )
    printf( "          Iavg, Iinst             :  IavgMin:%s IavgMax:%s\n", IavgMIN, IavgMAX )
    printf( "          Vtot                    :  VtotMin:%s VtotMax:%s\n", VtotMIN, VtotMAX )
    printf( "          SOH, SOC, Temp          :  SOHMin:%s SOHMax:%s\n", SOHMIN, SOHMAX )
    printf( "          Cylcnt                  :  CylcntMin:%s CylcntMax:%s\n", CylcntMIN, CylcntMAX )
    printf( "          BalT                    :  BalTMin:%s BalTMax:%s, and 0\n", BalTMIN, BalTMAX )
    printf( "          BalB                    :  BalBMin:%s BalBMax:%s, and 0\n", BalBMIN, BalBMAX )
    printf( "\n" )
    printf( "You may find out that some of Vx or Vtot have very low value, the acceptable Vx low is 2V, Vtot 16V, then you should use -v parameter setting as following:\n" )
    printf( "    %s -v VxMin=0 -v VtotMin=0 -v TicDiff=2000 anyRPIcsv.csv\n", awkpgm )
    printf( "       VxMin, VtotMin will use 0,0 (instead of default %d %d )\n", VxMIN, VtotMIN )
    printf( "       For unknown reason, the noise in RPI 2 I2C interface will cause Tic jump to very high value, and we may merge csv together from diffferent run, default TicDiff=1000 is a very safe number, but you can change to any number that suits you, in the above case, 2000 is used\n" )
    printf( "\n" )
    printf( "                                            %s %s  CYH %s\n\n", awkpgm, rev, pgm_date )
    exit
  }
  tmp_date = "tmp.tmp"
  system( "date > " tmp_date )
  while ( getline < tmp_date > 0 ) {
    time_stamp = $0
  }
  close( tmp_date )
  printf( "\n%s %s  Starts at %s\n", awkpgm, ARGV[1], time_stamp )
#  messsage1 = sprintf( "\n%s %s  Starts at %s", awkpgm, ARGV[1], time_stamp )
#  print message1
#  message( message1 )
  FS = "," 
  OFS = ","

  split( ARGV[1], fext, "." )
  Verr_file = sprintf( "V_%s_error.csv", fext[1] )
  err_file = sprintf( "tmp_%s.error", ARGV[1] )
  tmp_file = sprintf( "tmp_%s", ARGV[1] )
  C_file = sprintf( "C_%s", ARGV[1] )
  printf( "%s\n", header ) > Verr_file
  printf( "" ) > err_file
  printf( "%s\n", header ) > tmp_file
  printf( "%s\n", header ) > C_file
# V1 to V8
  for ( i=V1fld; i<=V1fld+7; i++ ) {
    ValMIN[i] = VxMIN
    ValMAX[i] = VxMAX
  }
# V1os
  ValMIN[V1osfld] = V1osMIN
  ValMAX[V1osfld] = V1osMAX
# chg
  ValMIN[chgfld] = chgMIN
  ValMAX[chgfld] = chgMAX
# disch
  ValMIN[chgfld+1] = dischMIN
  ValMAX[chgfld+1] = dischMAX
# Ref-, Ref+
  for ( i=Ref_fld; i<=Ref_fld+1; i++ ) {
    ValMIN[i] = VxMIN
    ValMAX[i] = VxMAX
  }
# Iavg
  ValMIN[Ref_fld+2] = IavgMIN
  ValMAX[Ref_fld+2] = IavgMAX
# Iinst
  ValMIN[Ref_fld+3] = IinstMIN
  ValMAX[Ref_fld+3] = IinstMAX
# Vtot
  ValMIN[Ref_fld+4] = VtotMIN
  ValMAX[Ref_fld+4] = VtotMAX
# V1_BG
  ValMIN[Ref_fld+5] = VxMIN
  ValMAX[Ref_fld+5] = VxMAX
# Temp
  ValMIN[Ref_fld+6] = TempMIN
  ValMAX[Ref_fld+6] = TempMAX
# SOH
  ValMIN[Ref_fld+7] = SOHMIN
  ValMAX[Ref_fld+7] = SOHMAX
# Cylcnt
  ValMIN[Ref_fld+8] = CylcntMIN
  ValMAX[Ref_fld+8] = CylcntMAX
# SOC
  ValMIN[Ref_fld+9] = SOCMIN
  ValMAX[Ref_fld+9] = SOCMAX
# BalB
  ValMIN[Ref_fld+10] = BalBMIN
  ValMAX[Ref_fld+10] = BalBMAX
# BalT
  ValMIN[Ref_fld+11] = BalTMIN
  ValMAX[Ref_fld+11] = BalTMAX
#USB csv         1    2  3  4  5  6  7  8  9  10   11  12    13   14   15   16    17   18    19   20  21     22  23   24   25   26
#           1    2    3  4  5  6  7  8  9  10 11   12  13    14   15   16   17    18   19    20   21  22     23  24   25   26   27  28
# header = "Tcnt,Time,V1,V2,V3,V4,V5,V6,V7,V8,V1os,chg,disch,Ref-,Ref+,Iavg,Iinst,Vtot,V1_BG,Temp,SOH,Cylcnt,SOC,BalB,BalT,Addr,Tic,dTic"
  cnt = 0
  errcnt = 0
#  TicDIFF = 1000
#06/30/2014 01:27:20 PM, 3.676, 3.668, 3.698, 3.617, 3.622, 3.691, 3.673, 3.653, 0.202, 1, 1, 2.585, 4.357,  7.864,  7.872, 29.298, 3.669, 38.8, 0, 0, 54, 4, 5, 0x50, 341254
#06/30/2014 01:27:33 PM, 3.677, 3.669, 3.699, 3.622, 3.627, 3.692, 3.681, 3.657, 0.201, 1, 1, 2.585, 4.357,  7.863,  7.871, 29.324, 3.671, 38.8, 0, 0, 54, 4, 5, 0x50, 341267
#06/30/2014 01:32:42 PM, 3.698, 3.697, 3.725, 3.647, 3.650, 3.722, 3.708, 3.687, 0.202, 1, 1, 2.585, 4.357,  7.864,  7.872, 29.534, 3.692, 39.4, 0, 0, 59, 4, 5, 0x50, 341576
#06/30/2014 01:34:53 PM, 3.695, 3.695, 3.722, 3.641, 3.647, 3.715, 3.708, 3.680, 0.202, 1, 1, 2.585, 4.357,  7.840,  7.851, 29.503, 3.690, 39.5, 0, 0, 60, 4, 5, 0x50, 341707

}

{ 
  if ( NR == 1 ) {
    print $0 >> C_file
  }
  else {
  prtokay = 1
  if ( NR == 2 ) {
    TicBase = 1 * $Ticfld
  }
  TicNum = 1 * $Ticfld
  if ( ( TicNum - TicBase ) > TicDIFF ) {
    prtokay = 0
  }
  else { 
    for ( i=V1fld; i<=V1fld+20; i++ ) {
      prtokay *= print10( $i, ValMIN[i], ValMAX[i] )
    }
    for ( i=V1fld+21; i<=V1fld+22; i++ ) {
      prtokay *= Zprint10( $i, ValMIN[i], ValMAX[i], "0" )
    }
    if ( NR != 1 ) {
      TicBase = TicNum
    }
  }

  if ( prtokay == 1 ) {
    tmp = $0
    cnt++
#    $1 = sprintf( "%d,%s", cnt, $1 )
    $1 = cnt
    print $0 >> C_file
#    printf( "%d,%s\n", NR, tmp ) >> tmp_file
    printf( "s\n", tmp ) >> tmp_file
#    $1 = sprintf( "%d,%s", NR, $1 )
#    print $0 >> tmp_file
  }
  else {
    tmp = $0
    errcnt++
#    $1 = sprintf( "%d,%s", errcnt, $1 )
    $1 = errcnt
    print $0 >> Verr_file
#    printf( "%d,%s\n", NR, tmp ) >> err_file
    printf( "%s\n", tmp ) >> err_file
#    $1 = sprintf( "%d,%s", NR, $1 )
#    print $0 >> err_file
  }
  }
}

END {
  if ( ARGV[1] != "" ) {
     printf( "\n%s  to the best knowledge, this file can be Veus-ed\n", C_file )
#    messsage1 = sprintf( "\n%s  to the best knowledge, this file can be Veus-ed\n", C_file )
#    print message1
     printf( "\n%s  is generated for abnormal lines, can be Veusz-ed graphically to see if some lines are thrown away wrong\n", Verr_file )
#    messsage1 = sprintf( "\n%s  is generated for abnormal lines, can be Veusz-ed graphically to see if some lines are thrown away wrong\n", Verr_file )
#    print message1
#    message( message1 )
     printf( "\nIf abnormal lines are thrown away wrong, then pairs files of %s %s can be used to construct back csv file\n", tmp_file, err_file )
#    messsage1 = sprintf( "\nIf abnormal lines are thrown away wrong, then pairs files of %s %s can be used to construct back csv file", tmp_file, err_file )
#    print message1
#    message( message1 )

    system( "date > " tmp_date )
    while ( getline < tmp_date > 0 ) {
      time_stamp = $0
    }
    close( tmp_date )
     printf( "\n%s %s  Ends   at %s\n\n", awkpgm, ARGV[1], time_stamp )
#    messsage1 = sprintf( "\n%s %s  Ends   at %s", awkpgm, ARGV[1], time_stamp )
#    print message1
#    message( message1 )
    system( "rm " tmp_date )
  }
}

function print10( item, min, max ) {
#  gsub( /^ *| *$/, "", item )
  item *= 1
  if ( ( item >= min ) && ( item <= max ) ) {
    return "1"
  }
  else {
    return "0"
  }
}

function Zprint10( item, min, max, Z ) {
#  gsub( /^ *| *$/, "", item )
  item *= 1
  if ( item == Z ) {
    return "1"
  }
  else {
    if ( ( item >= min ) && ( item <= max ) ) {
      return "1"
    }
    else {
      return "0"
    }
  }
}

#print "Serious error detected!" > "/dev/stderr"
function message( s ) {
  print s > "/dev/stderr"
#  print s | "cat 1>&2"
}

# print "Goodbye, World!" | "cat 1>&2" 
