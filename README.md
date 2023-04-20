# TMobile-GetNetworkStats
Get Network Statistics for T-Mobiles Arcadyan 5G Home Internet Router

# Requirements:
- Python 3 (This is tested on 3.9.13 & 3.9.2)
- Pandas (pip3 install pandas): https://pandas.pydata.org/
- plotly (pip3 install plotly): https://plotly.com/

# Set-Up

- Clone the branch:

```
git clone https://github.com/dy1lan/TMobile-GetNetworkStats.git
```
- Open up your command prompt and navigate to the directory where you cloned this Repo.
- Run `python3 GetInternetSpeeds.py`
- This will run continuously, grabbing data every 5 minutes and place it into the "Data" folder, until you do "CTRL + C" or exit the command prompt.

# Creating Plots from the CSV data

- Run  `python3 CSV-To-Graph.py`
- This will open up a file dialog to allow you to select a file, select one of the data files that were created by the "GetInternetSpeeds" script.
- Once selected, this will create a 4G and 5G graph of all the data that has been collected so far.

## 4G:
![image](https://user-images.githubusercontent.com/22224999/170891071-03f7609d-b947-47da-b3c5-9e6b798cb843.png)

## 5G: 
![image](https://user-images.githubusercontent.com/22224999/170891091-ecea98d8-4231-4e30-a35c-0908b4eaa145.png)

## Console Visuals:
![image](https://user-images.githubusercontent.com/22224999/233250094-d8aae862-4aa8-4f36-b37b-9c9b77068d3b.png)

# Notes:
- This has been tested and verified to be working on Windows and Raspberry Pi(Linux) so far.
