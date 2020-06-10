import cdsapi
import numpy as np
import os

c = cdsapi.Client()

# Here you define all the scripts parameters
stream =  'reanalysis-era5-pressure-levels'
day_list = ['01','02','03','04','05','06','07','08','09','10',
            '11','12','13','14','15','16','17','18','19','20',
            '21','22','23','24','25','26','27','28','29','30','31']
time = ['00:00','06:00','12:00','18:00']
file_fmt = 'netcdf'
target_grid = ['1.0','1.0']
yyyys = 1979
yyyye = 2019

yyyy = yyyys

while yyyy <= yyyye:
# for mm in ['01','02','03','04','05','06',
#           '07','08','09','10','11','12']:
 for mm in ['06','07','08','09','10','11','12']:

    fout = 'ERA5'+'_ta_'+'1.0deg_'+str(yyyy)+str(mm)

    c.retrieve(stream,{
    'variable'      : 'temperature',
    'product_type'  : 'reanalysis',
    'pressure_level': "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
    'year'          : yyyy,
    'month'         : mm,
    'day'           : day_list,
    'grid'          : target_grid,
    'time'          : time,
    'format'        : file_fmt
    }, fout+'.nc')

    os.system('cdo daymean '+fout+'.nc '+fout+'_day.nc')

 yyyy += 1
