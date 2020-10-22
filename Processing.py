"""Loads all the mesh data and saves it in a tidy table in feather form"""

import pandas as pd
import numpy as np

# Set the working directory as well as the names and 
root_folder = r"C:\Users\jamen\Google Drive\Everything\Results\P1 Model\OvenHeatFluxSensor\\"
sensors = ["Position1","Position2","Position3","Position4"] 
first_last = [0,60]
# name, first timestep, final timestep, timestep
areas = ["Sensor","Inlet","Outlet","Walls","BoundaryTC"] # prefix for each filename

alldata = []

for sensor in sensors:
    folder = root_folder + sensor
    timesteps = np.arange(first_last[0],first_last[1],1)
    for timestep in timesteps:
        for area in areas:
            filename = folder+"\\"+area+str(timestep)+".csv"
            df = pd.read_csv(filename,header=3,error_bad_lines=False)
            df["time"] = timestep*1
            df["area"] = area
            df["position"] = sensor[-1]
            alldata.append(df)
alldata = pd.concat(alldata)
column_names = {"X [ m ]":"x",
" Y [ m ]":"y",
" Z [ m ]":"z",
" Temperature [ K ]":"T",
" Wall Convective Heat Flux [ W m^-2 ]":"convective flux",
" Wall Heat Flux [ W m^-2 ]":"flux",
" Wall Heat Transfer Coefficient [ W m^-2 K^-1 ]":"HTC",
" Velocity u [ m s^-1 ]":"u",
" Velocity v [ m s^-1 ]":"v",
" Velocity w [ m s^-1 ]":"w",
" Pressure [ Pa ]":"P"
}

alldata = alldata.rename(columns=column_names)

print(alldata.columns)
alldata.loc[alldata["flux"]==" null","flux"] = np.nan
alldata.loc[alldata["convective flux"]==" null","convective flux"] = np.nan
alldata.loc[alldata["HTC"]==" null","HTC"] = np.nan

alldata["radiative flux"] = alldata["flux"] - alldata["convective flux"]

alldata = alldata.reset_index()
alldata.to_feather(root_folder+"alldata.feather")      