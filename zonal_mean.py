"""
Created on Thu May 7 2020 at ISMAR-CNR,
@author: Yassmin H.
        
        The code is calualte and plot the global zonal mean map of the upper Air temperature (latitude vs air pressure) 
"""

import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('ERA5_ta_1.0deg_197901-201912.nc')
print(ds)
ds=ds.t.mean(dim=['time','longitude']).plot.contourf(cmap='YlOrRd',levels=[180,195,210,225,240,255,270,285,300],cbar_kwargs=dict(orientation='horizontal',label='K'))
plt.yscale('log')
plt.ylabel('Level [hPa]')
plt.xlabel('Latitude [degree]')
plt.ylim(1000,1)
plt.axis('tight')
plt.show()
