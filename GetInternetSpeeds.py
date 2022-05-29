import json
import csv
import os, sys
import requests 
import time
from datetime import date
from datetime import datetime

while(True):
    try:
        today = date.today()
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        dateToday = today.strftime("%m-%d-%Y")

        path = os.path.abspath(os.path.dirname(sys.argv[0]))

        filename = "{0}/Data/{1}.csv".format(path, dateToday)

        url = requests.get("http://192.168.12.1/TMI/v1/gateway?get=signal")
        text = url.text

        data = json.loads(text)
        
        signal = data['signal']

        four_g = signal["4g"]
        five_g = signal["5g"]

        data_file = open(filename, 'a')

        csv_writer = csv.writer(data_file)

        if os.path.getsize(filename) == 0:
            Headers = ["Time","4G","Bands","Bars","Cell ID(CID)","eNBID","Reference Signal Received Power(RSRP)","Reference Signal Received Quality(RSRQ)","Received Signal Strength Indicator(RSSI)","Signal to Interference & Noise Ratio(SINR)","","5G","Bands","Bars","Cell ID(CID)","gNBID","Reference Signal Received Power(RSRP)","Reference Signal Received Quality(RSRQ)","Received Signal Strength Indicator(RSSI)","Signal to Interference & Noise Ratio(SINR)"]
            csv_writer.writerow(Headers)

        Values = [current_time, "", "(" + ",".join(four_g['bands']) + ")", four_g['bars'], four_g['cid'], four_g['eNBID'], four_g['rsrp'], four_g['rsrq'], four_g['rssi'], four_g['sinr'], "","", "(" + ",".join(five_g['bands']) + ")", five_g['bars'], five_g['cid'], five_g['gNBID'], five_g['rsrp'], five_g['rsrq'], five_g['rssi'], five_g['sinr']]
        csv_writer.writerow(Values)

        data_file.close()
    except Exception as ex:
        print("Error: " + str(ex))
    time.sleep(300)