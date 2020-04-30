'''
Created on Mon Feb 24 2020 11:30 at ISMAR-CNR,
@author: Federico S. and  Yassmin H.
The code is designed to plot the meridional circulation,
expressed by the stream function of the zonal mean meridional wind
and vertical velocity, in both annual and seasonal scale. 

'''

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import matplotlib.pyplot as plt

def meridional_wind():

    # Open dataset

    v_ds = xr.open_dataset('ERA5_v_wind_1.0deg_197901-201912.nc')

    # Get dimensions
    time = v_ds.time
    lev = v_ds.level
    lat = v_ds.latitude
    lon = v_ds.longitude

    def merid_circ(vlev,vlat,vvar):
        """Meridional circulation overview"""
        # Season selection and zonal averaging
        zm_vvar_ann = np.squeeze(vvar.mean(axis=3).to_array())
        zm_vvar_djf = np.squeeze(vvar.sel(time=vvar['time.season']=='DJF').mean(axis=3).to_array())   
        zm_vvar_jja = np.squeeze(vvar.sel(time=vvar['time.season']=='JJA').mean(axis=3).to_array())
  
        # Compute pressure layer thicknesses
        ext_vlev = np.array([0,0]+lev.values.tolist())
        dvlev = ext_vlev[1:-1]-ext_vlev[0:-2]

        # Thickness (Pa conversion)+ geometry weighting (cos lat and radius)
        dvlev_ext = np.zeros(np.shape(np.squeeze(zm_vvar_ann[0,:])))
        dvlev_ext[:,:] = dvlev[:,None]*np.cos(2*np.pi*vlat.values)
        zm_vvar_ann *= dvlev_ext*(2*np.pi*6371000.*100./9.81)*1E-10
        zm_vvar_djf *= dvlev_ext*(2*np.pi*6371000.*100./9.81)*1E-10
        zm_vvar_jja *= dvlev_ext*(2*np.pi*6371000.*100./9.81)*1E-10

        # Mask to adjust contour labels
        mask_ann = np.zeros(np.shape(zm_vvar_ann))
        mask_ann[:,:,:] = (np.abs(vlat)>80)
        zm_vvar_ann = np.ma.masked_where(mask_ann,zm_vvar_ann)
        mask_djf = np.zeros(np.shape(zm_vvar_djf))
        mask_djf[:,:,:] = (np.abs(vlat)>80)
        zm_vvar_djf = np.ma.masked_where(mask_djf,zm_vvar_djf)
        mask_jja = np.zeros(np.shape(zm_vvar_jja))
        mask_jja[:,:,:] = (np.abs(vlat)>80)
        zm_vvar_jja = np.ma.masked_where(mask_jja,zm_vvar_jja)
 
        plt.figure(figsize = (7,7))

        clevs = [-22,-18,-14,-10,-6,-4,-2,2,4,6,10,14,18,22]

        plt.subplot(3,1,1)
        psi_ann = plt.contour(vlat,vlev,np.mean(np.cumsum(zm_vvar_ann,axis=1),axis=0),\
                              levels=clevs,colors='k')
        plt.clabel(psi_ann,fmt='%1.0i')
        plt.ylim([max(vlev),min(vlev)])
        plt.xlim([-80,80]) 
        plt.ylabel('Level [hPa]')
        plt.title('Annual $\\psi$ [$10^{10}$ $kg/s$]')

        plt.subplot(3,1,2)
        psi_djf = plt.contour(vlat,vlev,np.mean(np.cumsum(zm_vvar_djf,axis=1),axis=0),\
                              levels=clevs,colors='k')
        plt.clabel(psi_djf,fmt='%1.0i')
        plt.ylim([max(vlev),min(vlev)])
        plt.xlim([-80,80]) 
        plt.ylabel('Level [hPa]')
        plt.title('DJF')

        plt.subplot(3,1,3)
        psi_jja = plt.contour(vlat,vlev,np.mean(np.cumsum(zm_vvar_jja,axis=1),axis=0),\
                              levels=clevs,colors='k')
        plt.clabel(psi_jja,fmt='%1.0i')
        plt.ylim([max(vlev),min(vlev)])
        plt.xlim([-80,80]) 
        plt.ylabel('Level [hPa]')
        plt.xlabel('Latitude [degree]')
        plt.title('JJA')

        plt.tight_layout() 
        plt.savefig('merid_cells_ann_seas.png',format='png') 
    
    merid_circ(lev,lat,v_ds)
if __name__ == '__main__':
    meridional_wind()
