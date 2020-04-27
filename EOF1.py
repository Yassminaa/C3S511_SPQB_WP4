'''
Created on Fri Feb 21 13:30:59 2020 at ISMAR-CNR,

@author: Yassmin H.

The code is designed to cacluate EOF1 expressed as the covariance 
between the PCs and the time series of the Eof input dataset for 
the Zonal wind following methodology presented in (LORENZ et al.,2001) 
https://journals.ametsoc.org/doi/full/10.1175/1520-0469%282001%29058%3C3312%3AEZFFIT%3E2.0.CO%3B2
'''
import numpy as np
import xarray as xr
import math
import matplotlib.pyplot as plt
from eofs.xarray import Eof

#Open dataset of Southern Hemisphere zonal-wind and calculte leap year 
ds = xr.open_dataset('SH_ERA5_ua_1000-100_197901-201912_day.nc')
ds = ds.sel(time=~((ds.time.dt.month == 2) & (ds.time.dt.day == 29)))

#Calculate daily anomaly data by removing the mean seasonal cycle.
seas_cycle = ds.groupby('time.day').mean('time')
anomaly    = ds.groupby('time.day') - seas_cycle

#Zonal mean the anomaly data.
zonal_mean = anomaly.u.mean(dim=['lon'])

#Calculate weighted EOF1 of the zonal-mean zonal wind of daily anomaly
coslat = np.cos(np.deg2rad(zonal_mean.coords['lat'].values)).clip(0., 1.)
wgts   = np.sqrt(coslat)                                             # Weight latitude  

solver = Eof(zonal_mean,weights=wgts)

x=math.ceil(100*solver.varianceFraction(neigs=1).values)           # Find total variance % of EOF1 

#(EOF1 expressed as the covariance between the PCs and the time series of the Eof input dataset 
eof1 = solver.eofsAsCovariance(neofs=1)                             

#plot results and show it
eof1[0,:,:].plot.contourf(cmap='BrBG_r',levels=8)
plt.title('EOF#1 of  [u], m/s            '+''.join(str(x))+'%')
plt.ylim(bottom=1000,top=100)
plt.tight_layout()
plt
