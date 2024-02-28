#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:00:00 2024

@author: kate
"""
import xarray as xr
import pandas as pd
import numpy as np
file2load='./maunakea_topo_03s.nc'
# Specify the file path where you want to save the CSV file
file_path = 'maunakea.topo'

# read topo from netcdf
grid = xr.open_dataset(file2load)
#convert to pandas DF
df_grid = grid.to_dataframe().sort_values('lat').reset_index()
lat_vec=pd.unique(df_grid['lat'])
lon_vec=pd.unique(df_grid['lon'])

df_sorted=df_grid[df_grid['lat']==df_grid['lat'][0]].sort_values('lon').to_numpy()
for lat in lat_vec[1:]:
    df_sorted=np.vstack((df_sorted,df_grid[df_grid['lat']==lat].sort_values('lon').to_numpy()))

df_sorted=pd.DataFrame(df_sorted)                        
# add nb lon nb lat as first line
custom_first_line = f"{len(grid.lon.data)} {len(grid.lat.data)}"


# Open the file in write mode and add the custom first line
with open(file_path, 'w') as file:
    file.write(custom_first_line + '\n')

# Append the DataFrame to the CSV file
df_sorted.to_csv(file_path, mode='a', index=False, header=False, sep=' ')