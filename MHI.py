'''
Created on Mon Mar 02 2020 10:30 at ISMAR-CNR,
@author: Federico S. and  Yassmin H.
The code is designed to plot the the Monsoon Hadley Index (MHI)
as described ni (Goswami et al., 1999) 
https://doi.org/10.1002/qj.49712555412

'''
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt


def meridional_wind():

    # Open datset

    v_ds = xr.open_dataset('ERA5_v_wind_1.0deg_197901-201912.nc')

    # Get dimensions
    time = v_ds.time
    lev  = v_ds.level
    lat  = v_ds.latitude
    lon  = v_ds.longitude

    def mh_index(vtime,vlev,vlat,vlon,vvar):
        """Monsoon Hadley index computation"""

        def is_jjas(month):
            return (month >= 6) & (month <= 9)

        # Regional and height selection
        vvar = vvar.groupby('time.month')-vvar.groupby('time.month').mean('time')
        mh_vvar = vvar.sel(level=850) - vvar.sel(level=200)
        vlat = vlat[np.where(np.logical_and(vlat>=10,vlat<=30))]
        vlon = vlon[np.where(np.logical_and(vlon>=70,vlon<=110))]
        
        mh_vvar = mh_vvar.sel(latitude=vlat)
        mh_vvar = mh_vvar.sel(longitude=vlon)

        # Season selection and average
        mh_seas = np.squeeze(mh_vvar.sel(time=is_jjas(mh_vvar['time.month'])))
        mh_seas = mh_seas.groupby('time.year').mean('time')
        vtime = mh_seas.year

        coslat = xr.DataArray(np.abs(np.cos(vlat*np.pi/180.)),coords=[vlat],dims=['latitude'])

        mh_seas = mh_seas.mean('longitude') #(axis=2) # lon
        mh_seas *= coslat/np.sum(coslat) # latitude weighting
        mh_seas = mh_seas.mean('latitude') #(axis=1)
           
        mh_seas = np.squeeze(mh_seas.to_array().values)
        mh_seas_mea = np.mean(mh_seas,axis=0)
        mh_seas_std = np.std(mh_seas,axis=0,ddof=1)  
        mh_seas = (mh_seas-mh_seas_mea)/mh_seas_std # standardization

        plt.figure(figsize=(7,3))
        plt.plot(vtime,mh_seas,'k')
        plt.plot(vtime[np.where(mh_seas>0)],mh_seas[np.where(mh_seas>0)],ls='',marker='o',color='r')
        plt.plot(vtime[np.where(mh_seas<0)],mh_seas[np.where(mh_seas<0)],ls='',marker='o',color='b')
        plt.axhline(0,color='gray',zorder=0) 
        plt.xlim([min(vtime),max(vtime)])
        plt.ylim([-2.5,2.5])
        plt.ylabel('standard deviation')
        plt.title('Monsoon Hadley Index')

        plt.tight_layout()
        plt.show()
        plt.savefig('mh_index.png',format='png')

        return()

    mh_index(time,lev,lat,lon,v_ds)

if __name__ == '__main__':
    meridional_wind()
