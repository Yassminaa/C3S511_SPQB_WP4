'''
Created on Mon Feb 24 2020 15:00 at ISMAR-CNR,
@author: Federico S. and  Yassmin H.
The code is designed to plot the seasonal global map
of meridional wind component at a selected level . 

'''

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt
import pandas


def meridional_wind():

        # Open dataset
        
        v_ds = xr.open_dataset('ERA5_v_wind_1.0deg_197901-201912.nc')
        time = v_ds.time
        lev = v_ds.level
        lat = v_ds.latitude
        lon = v_ds.longitude

        def glob_map(vlat,vlon,vvar,levsel):
             vvar = vvar.sel(level=levsel)
             
             djf=vvar.where(vvar['time.season'] == 'DJF').mean('time')
             jja=vvar.where(vvar['time.season'] == 'JJA').mean('time')
             vvar_djf = np.squeeze(djf.to_array().values)
             vvar_jja = np.squeeze(jja.to_array().values)


             fig_map = plt.figure(figsize=(5.5,3.5))
             clevs = -3+np.arange(21)*0.3 # m/s

             #fig, ax1,ax2 = plt.subplots(2,1,sharex=True) #

             # DJF mean conditions
             ax1 = fig_map.add_subplot(2,1,1,projection=ccrs.PlateCarree())
             ax1.coastlines()
             up_contf = plt.contourf(vlon,vlat,vvar_djf,levels=clevs,extend='both',cmap='BrBG_r')
             ax1.set_extent([-180,180,-60,60])
             plt.title('December-January-February   %i hPa' % levsel)

             # JJA mean conditions
             ax2 = fig_map.add_subplot(2,1,2,projection=ccrs.PlateCarree())
             ax2.coastlines()
             plt.contourf(vlon,vlat,vvar_jja,levels=clevs,extend='both',cmap='BrBG_r')
             ax2.set_extent([-180,180,-60,60])
             plt.title('June-July-August   %i hPa' % levsel)
             ax1.set_aspect('auto')
             ax2.set_aspect('auto')

             # Shared colorbar
             cbar_ax = fig_map.add_axes([0.91, 0.15, 0.02, 0.7])
             cbar = fig_map.colorbar(up_contf, cax=cbar_ax)
             cbar.ax.tick_params(labelsize=7)
             cbar.ax.set_title('     [m/s]',fontsize=9)
             fig_map.subplots_adjust(hspace=0.2, wspace=0.0)
             plt.tight_layout() 
             plt.savefig('map_monsoon2_'+str(levsel)+'hPa.png',format='png')

             return()

        glob_map(lat,lon,v_ds,850)
        
if __name__ == '__main__':
    meridional_wind()
