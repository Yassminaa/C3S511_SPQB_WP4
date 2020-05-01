'''
Created on Mon Feb 3 2020 09:30 at ISMAR-CNR,
@author: Yassmin H.
The code plots the monthly climatology mean for zonal wind
(month vs pressure in log scale)

'''

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def average(self, dim=None, weights=None):
    if weights is None:
        return self.mean(dim)
    else:
        return (self * weights).sum(dim) / weights.sum(dim)

# Open dataset (in case of regional calculations cut the target domain and open it)
 
ds=xr.open_dataset('ERA5_u_wind_1.0deg_197901-201912_30N-30S.nc')
ds=ds.groupby('time.month').mean('time')
clim=ds.mean(dim='longitude')

W_lat=np.cos(np.pi*clim.latitude/180)					#weighted latitude 

clim_avg=average(clim,dim='latitude',weights=W_lat)				#Latitude weighted average

#Produce plot (pressure vs month)
clim_avg.u.plot.contourf(x='month',y='level',cmap='BrBG_r',extend='both',levels=[-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40],cbar_kwargs=dict(orientation='horizontal',label=''))
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))
plt.xticks(clim_avg.u.month,labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],rotation=0)
plt.ylabel('Level  [hPa]')
plt.xlabel(' ')
plt.title(' ERA5 climatology of zonal wind [30° N - 30° S]')
plt.ylim (1000,0)
plt.yscale('log')
plt.axis('tight')
plt.tight_layout()
plt.show()	

