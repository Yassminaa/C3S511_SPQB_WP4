'''
Created on Wed Feb 05 2020 11.30 at ISMAR-CNR,

@author: Yassmin H. and Federico S.
        
        The code is designed to show JET latitude index, select the preferred JET 
        latitude(s)and show composites of the zonal wind  for those locations 
        based on the methodology presented in (Woollings et al., 2010)
        https://doi.org/10.1002/qj.625
        
'''
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.signal import argrelextrema
import seaborn as sns
import os
import cftime
import datetime
import pandas as pd
import nc_time_axis

from cftime import DatetimeNoLeap
from cdo import Cdo
cdo = Cdo()

# Calculate the zonal mean over a longitudinal sector (0° - 60°W for the North Atlantic) to the vertical mean of ua at the levels from (925 to 700 mba)
cdo.zonmean(input='-vertmean -del29feb DAILY_NH_jetregion.nc', output='Zonmean_vertmean.nc')

# Calculate lowpass filtered 6 days (10 days with a window of 61 days)
cdo.lowpass("%f" % (6.), input='Zonmean_vertmean.nc', output='lowpass.nc')
os.system('rm Zonmean_vertmean.nc') # remove file

# Open the low-pass filtered file
jet_reg = xr.open_dataset('lowpass.nc')

# Remove lon dimintion from the file and select DJF 
jet_reg = jet_reg.mean('lon').sel(time=(jet_reg['time.season'] == 'DJF'))

# Select the westerly wind only
jet_reg = jet_reg.where(jet_reg.u>=0,drop=True).squeeze()

# Get dimensions as DataArrays
#time =jet_reg.time
time= jet_reg.indexes['time'].to_datetimeindex()
lat = jet_reg.lat

# Define the JLI as a numpy array
lat_max = np.zeros(len(time),dtype='f')

# Find latitude of maximum westerly wind speed at each step
for itim in range(len(time)):
            lat_max[itim] = lat[np.where(jet_reg.isel(time=itim).to_array()==jet_reg.isel(time=itim).max(dim='lat').to_array())[1]].values

# Save the results into a new dataset for further use
jli_ds = xr.DataArray(lat_max,coords=[time],dims=['time'])
jli_ds.name = 'JLI'
print(jli_ds)


# Seasonal climatology & anomaly
jli_clim = jli_ds.groupby('time.day').mean('time')
jli_anom = jli_ds.groupby('time.day') - jli_clim

# Plot the histogram for the JLI anomaly with the kernel distribution estimation
sns.distplot(jli_anom, hist=True, bins= 18,hist_kws={'edgecolor':'black'},kde=True,norm_hist=True)
plt.xlabel('Latitude anomaly [degrees]')
plt.ylabel('Normalized frequency')
plt.show()

'''
The following part is considered as a seconde part of the code
it designed to define latitude(s) of the maxima in JLI and shows
the composites of the zonal-wind in the preferred jet stream locations
'''
# Define latitude(s) of the maxima in JLI by make a kde estimate and define ancillary lat, equally spaced (100 lats here)

#jli_dss=xr.open_dataset('saved_on_disk.nc')
lat_kde = gaussian_kde(jli_ds)
lat_x = np.linspace(jli_ds.min(),jli_ds.max(),num=100)
maxima_lats=lat_x[argrelextrema(lat_kde(lat_x),np.greater)]
print(maxima_lats)

# Open full file of northern hiemsphere over longitue(0 - 60°W) and all tropospheric vertical levels
f=('JET_ERA5_u_wind_1.0deg_197901_201912_daily_levels.nc')
full_ds=xr.load_dataset(f)
full_ds =full_ds.sel(time=(full_ds['time.season'] == 'DJF'))

# iterate over the maxima latiude and calculte the composites
for iloc in range(len(maxima_lats)):

    maxi=maxima_lats[iloc]
    loc=jli_ds.where((jli_ds<=maxi+0.5) & (jli_ds>=maxi-0.5) )                     # define +/- 0.5° range of maxima location  
    loc=loc.dropna('time', how='all')
    print(loc.time) 
    JET_loc=full_ds.where(full_ds.time==loc.time,drop=True).squeeze()              # Select the dates of jet latiudes 
    JET_loc=JET_loc.dropna('time', how='all')
    print(JET_loc.time)
    JET_loc=JET_loc.mean(dim=['longitude','time'])                                # mean  over time and longtiues
   
    # Plot results
    JET_loc.u.plot.contourf(vmin= 5,levels= [5., 10., 15., 20., 25., 30.], extend = 'max',cmap='YlGnBu')
    plt.ylabel('Level [hPa]')
    plt.xlabel('Latitude [degrees]')
    plt.ylim(bottom=1000, top=100)
    plt.title("Jet location is {:.1f}".format(maxi))
    plt.tight_layout()
    plt.show()
