import json
import csv
import os, sys
import requests 
import time
import threading
import pytz
from datetime import datetime

HAS_PRINTED = False

class TextColors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

def CleanUpPreviousResults():
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(21):
        print(LINE_UP, end=LINE_CLEAR) # Moves the cursor up and clears that line.

def CheckRSRP(rsrp):
    return GetColor(rsrp, -80, -90)

def CheckRSRQ(rsrq):
    return GetColor(rsrq, -10, -15)

def CheckRSSI(rssi):
    return GetColor(rssi, -75, -80)

def CheckSINR(sinr):
    return GetColor(sinr, 20, 15)

def GetColor(value_to_check, ok, warn):
    value = int(value_to_check)
    if(value > ok):
        return f"{TextColors.OKGREEN}{value_to_check}{TextColors.END}"
    
    if(value > warn):
        return f"{TextColors.WARNING}{value_to_check}{TextColors.END}"
    
    return f"{TextColors.FAIL}{value_to_check}{TextColors.END}"

def PrintResults(current_time, four_g_bands, four_g_bars, four_g_cid, four_g_eNBID, four_g_rsrp, four_g_rsrq, four_g_rssi, four_g_sinr, five_g_bands, five_g_bars, five_g_cid, five_g_gNBID, five_g_rsrp, five_g_rsrq, five_g_rssi, five_g_sinr):
    global HAS_PRINTED
    if (HAS_PRINTED):
        CleanUpPreviousResults() # This allows for updates on the same lines so that the user doesn't have to continuously scroll down.

    print(
        f"                                           4G\n" +
        f"                                      Bands : {four_g_bands}\n" +
        f"                                       Bars : {four_g_bars}\n" +
        f"                               Cell ID(CID) : {four_g_cid}\n" +
        f"                                      eNBID : {four_g_eNBID}\n" +
        f"      Reference Signal Received Power(RSRP) : {CheckRSRP(four_g_rsrp)}\n" +
        f"    Reference Signal Received Quality(RSRQ) : {CheckRSRQ(four_g_rsrq)}\n" +
        f"   Received Signal Strength Indicator(RSSI) : {CheckRSSI(four_g_rssi)}\n" +
        f" Signal to Interference & Noise Ratio(SINR) : {CheckSINR(four_g_sinr)}\n" +
        f"\n" +
        f"                                           5G\n" +
        f"                                      Bands : {five_g_bands}\n" +
        f"                                       Bars : {five_g_bars}\n" +
        f"                               Cell ID(CID) : {five_g_cid}\n" +
        f"                                      gNBID : {five_g_gNBID}\n" +
        f"      Reference Signal Received Power(RSRP) : {CheckRSRP(five_g_rsrp)}\n" +
        f"    Reference Signal Received Quality(RSRQ) : {CheckRSRQ(five_g_rsrq)}\n" +
        f"   Received Signal Strength Indicator(RSSI) : {CheckRSSI(five_g_rssi)}\n" +
        f" Signal to Interference & Noise Ratio(SINR) : {CheckSINR(five_g_sinr)}\n" +
        f"\n" +
        f"                               Last Updated : {current_time}")
    HAS_PRINTED = True

def GetSpeeds():
    sleepThread = threading.Thread(target=StartWriterSleep, daemon=True)
    while(True):
        utc_datetime = datetime.now(pytz.timezone('UTC'))
        est_time = utc_datetime.astimezone(pytz.timezone('US/Eastern')).now()

        current_time = est_time.strftime("%H:%M:%S")
        dateToday = est_time.strftime("%m-%d-%Y")
        try:
            path = os.path.abspath(os.path.dirname(sys.argv[0]))

            filename = "{0}/Data/{1}.csv".format(path, dateToday)

            url = requests.get("http://192.168.12.1/TMI/v1/gateway?get=signal")
            text = url.text

            data = json.loads(text)
            
            signal = data['signal']

            four_g = signal["4g"]
            five_g = signal["5g"]
            four_g_bands = "(" + ",".join(four_g['bands']) + ")"
            five_g_bands = "(" + ",".join(five_g['bands']) + ")"

            # If the thread is not waiting then we can write again.
            if not sleepThread.is_alive():
                data_file = open(filename, 'a')
                csv_writer = csv.writer(data_file)

                if os.path.getsize(filename) == 0:
                    Headers = ["Time","4G","Bands","Bars","Cell ID(CID)","eNBID","Reference Signal Received Power(RSRP)","Reference Signal Received Quality(RSRQ)","Received Signal Strength Indicator(RSSI)","Signal to Interference & Noise Ratio(SINR)","","5G","Bands","Bars","Cell ID(CID)","gNBID","Reference Signal Received Power(RSRP)","Reference Signal Received Quality(RSRQ)","Received Signal Strength Indicator(RSSI)","Signal to Interference & Noise Ratio(SINR)"]
                    csv_writer.writerow(Headers)

                Values = [current_time, "", four_g_bands, four_g['bars'], four_g['cid'], four_g['eNBID'], four_g['rsrp'], four_g['rsrq'], four_g['rssi'], four_g['sinr'], "","", five_g_bands, five_g['bars'], five_g['cid'], five_g['gNBID'], five_g['rsrp'], five_g['rsrq'], five_g['rssi'], five_g['sinr']]
                csv_writer.writerow(Values)
                data_file.close()

                # Threads can't be reran so we have to create it and run it again.
                sleepThread = threading.Thread(target=StartWriterSleep, daemon=True)
                sleepThread.start()

            # Print the current, real-time, data out to the user in the console.
            PrintResults(current_time, four_g_bands, four_g['bars'], four_g['cid'], four_g['eNBID'], four_g['rsrp'], four_g['rsrq'], four_g['rssi'], four_g['sinr'], five_g_bands, five_g['bars'], five_g['cid'], five_g['gNBID'], five_g['rsrp'], five_g['rsrq'], five_g['rssi'], five_g['sinr'])
            
        except Exception as ex:
            print(str(dateToday) + " " + str(current_time) + " : Error: " + str(ex))
        time.sleep(5) # Waits 5 seconds so that we aren't overloading the webpage.

def StartWriterSleep():
    time.sleep(300) # Waits 300 seconds or 5 minutes. This can be adjusted to however the user sees fit.
    return
    


GetSpeeds()