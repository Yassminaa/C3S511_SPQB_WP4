
"""
Created on Thu May 7 2020 at ISMAR-CNR,
@author: Yassmin H.,
        
        The code is plotting the anomaly of the upper Air temperature (time vs air pressure) 
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter 
import matplotlib.dates as mdates
import iris
from iris.analysis import Aggregator
import iris.coord_categorisation
from iris.analysis import stats as cubestats
import iris.coords as icoords
import iris.quickplot as qplt
import numpy as np


def main():
    
    fname = 'ERA5_ta_1.0deg_197901-201912.nc' 		# Open dataset

    cube = iris.load_cube(fname)
    ta = cube
    clim = cube.copy()
    iris.coord_categorisation.add_month_number(clim, 'time', name='month_num')

#Climatology calculation
    clim_comp = clim.aggregated_by('month_num', iris.analysis.MEAN)  		
    clim_anom = clim.copy()    
    
#Anomaly calculation                       
    for mn in range(len(clim_anom.coord('month_num').points)):
                
        idx = clim_comp.coord('month_num').points.tolist().index(clim_anom.coord('month_num').points[mn])
                                    
                                               
        clim_anom.data[mn,:,:,:] = \
        clim_anom.data[mn,:,:,:] - clim_comp.data[idx,:,:,:]


# produce plot (pressure vs time)                
 
    clim_anom.coord('latitude').guess_bounds() # put lat/lon bounds to the dataset
    clim_anom.coord('longitude').guess_bounds()

    Anom = clim_anom.collapsed(['longitude','latitude'], iris.analysis.MEAN,weights=iris.analysis.cartography.area_weights(clim_anom))
    plt.yscale('log',basey=10)
    levels=[-2.0,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1,1.25,1.5,1.75,2.0]
    qplt.contourf(Anom,cmap='RdBu_r',extend='both', levels=levels)
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # date format on x-axis      
    plt.ylabel('Level  [hPa]')
    plt.axis('tight')
 
    plt.show()


if __name__ == '__main__':

    main()
