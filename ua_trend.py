'''
Created on Mon Mar 02 2020 15:00 at ISMAR-CNR,
@author: Federico S. and  Yassmin H.
The code is designed to estimate and plot
the DJF global linear trend (shading) and 
zonal mean (contours) of zonal wind

'''

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt


def ua_trend():

   # open dataset
    u_ds = xr.open_dataset('DJF_ERA5_u_wind_1.0deg_197901-201912_seasmean.nc')
  
    # Get dimensions
    time = u_ds.time
    lev = u_ds.level

    u_sel = u_ds.where(u_ds['time.season'] == 'DJF')

    # Get dimensions (after selection)
    lat = u_sel.latitude
    lon = u_sel.longitude
    u_sel = u_sel.groupby('time.year').mean('time')
    u_sel = u_sel.mean(axis=3) 
    time = u_sel.year

    u_sel = np.squeeze(u_sel.to_array().values)

    # Discard first and last (incomplete) seasons
    u_sel = u_sel[1:-1,::]
    time = time[1:-1]

    u_slope = np.zeros((len(lev),len(lat)),dtype='f')
    u_intcp = np.zeros((len(lev),len(lat)),dtype='f')

    # Reshape the input as (time,space)
    u_ref = np.copy(np.reshape(u_sel,(len(time),len(lev)*len(lat))))
    u_slope, u_intcp = np.polyfit(np.arange(len(time)),u_ref,1)

    # Go back to lat-lon shape
    u_slope = np.reshape(u_slope,(len(lev),len(lat)))
    u_intcp = np.reshape(u_intcp,(len(lev),len(lat)))

   # plt.figure(figsize=(4,3.5,))

    plt.contourf(lat,lev,np.mean(u_sel,axis=0),levels=[-40,-30,-20,-10,0,10,20,30,40],cmap='BrBG_r',extend='both')
    plt.contour(lat,lev,u_slope*10,levels=[-1.8,-1.2,-0.6,0.2,0,0.2,0.6,1.2,1.8],colors='k', inline=True)
    plt.ylim([max(lev),10])
    plt.xlim([-90,90])
    plt.yscale('log',basey=10)
    plt.xticks([-90,-60,-30,0,30,60,90],[-90,-60,-30,0,30,60,90])
    plt.xlabel('Latitude [degree]')
    plt.ylabel('Level [hPa]')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig('ua_global_trend_djf.png',format='png')

if __name__ == '__main__':
    ua_trend()


