'''
Created on Fri Feb 28 2020 15:00 at ISMAR-CNR,
@author: Federico S. and  Yassmin H.
The code is designed to plot the zonal mean of the meridional wind 
in the region 10° N - 30° N and 70° E - 110° E (South Asian monsoon)
for both DJF and JJA 

'''

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt



def meridional_wind():

    # Open dataset

    v_ds = xr.open_dataset('ERA5_v_wind_1.0deg_197901-201912_mon.nc')

    # Get dimensions
    time = v_ds.time
    lev = v_ds.level
    lat = v_ds.latitude
    lon = v_ds.longitude


    def msa_section(vtime,vlev,vlat,vlon,vvar):
        #vvar = vvar.sel(level=levsel)
        
        """South Asian monsoon latitude-pressure view"""
        # Region selection and zonal mean
        vlat = vlat[np.where(np.logical_and(vlat>9,vlat<31))]
        vlon = vlon[np.where(np.logical_and(vlon>69,vlon<111))]
        msa_vvar = v_ds.sel(latitude=vlat)
        msa_vvar = msa_vvar.sel(longitude=vlon)
        msa_vvar = msa_vvar.mean(axis=3) 

        #print (msa_vvar)
        # Season selection
        msa_vvar_djf = np.squeeze(msa_vvar.sel(time=vvar['time.season']=='DJF').to_array())
        #print(msa_vvar_djf)
        msa_vvar_jja = np.squeeze(msa_vvar.sel(time=vvar['time.season']=='JJA').to_array())

        clevs = (-10 + np.arange(21))*.5
        plt.figure(figsize=(5,3))
        plt.subplot(1,2,1)
        va=plt.contourf(vlat,vlev,np.mean(msa_vvar_djf,axis=0),levels=clevs,cmap='BrBG_r',extend='both')
        plt.ylim([max(vlev),min(vlev)])
        plt.ylabel('Level [hPa]')
        plt.xlabel('Latitude [degree]')
        plt.xticks([10,15,20,25,30])
        plt.title('DJF')
        plt.subplot(1,2,2)
        plt.contourf(vlat,vlev,np.mean(msa_vvar_jja,axis=0),levels=clevs,cmap='BrBG_r',extend='both')
        plt.ylim([max(vlev),min(vlev)])
        plt.xlabel('Latitude [degree]')
        plt.xticks([10,15,20,25,30])
        plt.title('JJA')
        cbar = plt.colorbar(va)
        plt.tight_layout()
        plt.savefig('msa_section.png',format='png')

        return()

  
    msa_section(time,lev,lat,lon,v_ds)

if __name__ == '__main__':
    meridional_wind()

