"""
Created on Thu May 7 2020 at ISMAR-CNR,
@author: Yassmin H.
        
        The code is calualte and plot the standard deviation of the daily anomaly of the upper Air temperature (latitude vs air pressure) 
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


#Open dataset
ds = xr.open_dataset('ERA5_ta_1.0deg_197901-201912.nc')
ds=ds.sel(time=~((ds.time.dt.month == 2) & (ds.time.dt.day == 29))) # remove 29feb 

#Daily anomaly
climatology = ds.groupby('time.day').mean('time')
anomaly	= ds.groupby('time.day')-climatology

Anom=anomaly.mean(dim=['longitude'])
Anom=Anom.std(dim='time')  #standard deviation 

#plot result

Anom.t.plot.contourf(x='latitude',y='level',cmap='Wistia',extend='both', levels=[0,1,2,3,4,5,6,7,8,9,10],cbar_kwargs=dict(orientation='horizontal',label='K'))
plt.ylabel('Level  [hPa]')
plt.xlabel('Latitude [degree]')
plt.ylim(1000,1)
plt.yscale('log')
plt.axis('tight')
plt.show()
