import pandas as pd
import plotly.express as px
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

Tk().withdraw()
file_path = askopenfilename()
filename = os.path.basename(file_path)
if not filename.endswith(".csv"):
    print("\n\n*******ERROR: File must be a csv produced from GetInternetSpeeds.py.*******")
    exit()

df = pd.read_csv(file_path)

Four_G_eNBID = df["eNBID"]
Four_G_Bands = df.columns[2]

Five_G_gNBID = df["gNBID"]
Five_G_Bands = df.columns[12]

df.drop("eNBID", axis=1, inplace=True)
df.drop("gNBID", axis=1, inplace=True)

fig = px.line(df, x=df['Time'], y=df.columns[3:9])
fig2 = px.line(df, x=df["Time"], y=df.columns[12:18])

fig.update_layout(title='4G Stats for {0}'.format(filename),
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)
fig2.update_layout(title='5G Stats for {0}'.format(filename),
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True)

fig.show()
fig2.show()

