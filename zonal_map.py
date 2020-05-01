"""
Created on Mon Feb 03 2020 13:30 at ISMAR-CNR,
@author: Yassmin H.
The code plots the annual and seasonal 
zonal maps of zonal wind component
"""

import iris
from iris.analysis import Aggregator
import iris.coord_categorisation
import iris.coords as icoords
import iris.quickplot as qplt
import matplotlib.pyplot as plt

# Open dataset file and load as a cube 
fname = 'ERA5_u_wind_1.0deg_197901-201912.nc'
cube = iris.load_cubes(fname)
u = cube[0]

'''  
# This block if seasonl (DJF/JJA) plots is required. Just remove the block and replace the 'annual' by the name of season
    #add season coordinate and extract (DJF/JJA)
    iris.coord_categorisation.add_season(u, 'time', name='season')
    djf = u.extract(iris.Constraint(season='djf'))
    jja = u.extract(iris.Constraint(season='jja'))
'''

#plot = 'lat_time'   #latitude/time plots
plot = 'lat_lev'    #latitude/level plots (zonal mean plot)
#plot = 'time_lev'   #time/level plots

if plot == 'lat_time':
    annual = u.collapsed(['longitude','air_pressure'], iris.analysis.MEAN) 

if plot == 'lat_lev':
    annual = u.collapsed(['longitude','time'], iris.analysis.MEAN)
    plt.yscale('log',basey=10)                  # plot logarithmic air_pressure scale 
  
if plot == 'time_lev':
    annual = u.collapsed(['latitude','longitude'], iris.analysis.MEAN,weights=iris.analysis.cartography.area_weights(u))  
    plt.yscale('log',basey=10)                  # plot logarithmic air_pressure scale

# plot results
qplt.contourf(annual,cmap='BrBG_r',vmax =40, vmin=-40, levels=[-40,-30,-20,-10,0,10,20,30,40], extend='both')
plt.ylabel('Level [hPa]')
plt.xlabel('Latitude [degree]')
plt.axis('tight')
plt.show()
