# Python 3.7.10
# 31.05.21
#############
# Make emissionfiles per model per region as designed in the script regiondefinitions.py
# You also need the file pathfinder.py and the noresmdata has to have been mounted as follows:
# sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ noresmdata/
# on Betzy
#############
import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
import warnings
import cartopy.crs as ccrs
import cftime

warnings.simplefilter("ignore")
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'


def lookup(fullpath, var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    list_of_data = []
    for file in glob.glob(fullpath):
        #print(file)
        opendata = xr.open_dataset(file,decode_times=True, use_cftime=True)[var]
        list_of_data.append(opendata)
    if len(list_of_data) > 1:
        #print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(list_of_data,dim='time')
        opendata = concatted.sortby('time')
    elif len(list_of_data)==0:
        print('NO MATCHES FOR THIS PATH', fullpath)
        sys.exit()
    else:
        opendata = list_of_data[0]
    return opendata

def regionfixer(area,reg_info):
    # This function fixes the longitude values if they are negative, since xarray only operates with longitudinal values between 
    # 0 and 360, not -180 to 180. It also checks if the area crossed the meridional line, and if so returns "True" for cyclic
    # So this can be handled in the boolean way later
    #--------------------------------------
    if reg_info['lonA'] < 0:
        oldlon = reg_info['lonA']
        newlonA = reg_info['lonA'] + 360
        print('Longitude value A for ',area,' was ',oldlon,' but is now ',newlonA)
    else:
        newlonA = reg_info['lonA']
        
    if reg_info['lonB'] < 0:
        oldlon = reg_info['lonB']
        newlonB = reg_info['lonB'] + 360
        print('Longitude value B for ',area,' was ',oldlon,' but is now ',newlonB)    
    else:
        newlonB = reg_info['lonB']
    
    if newlonA > newlonB:
        cyclic = True
    else:
        cyclic = False
    
    return newlonA, newlonB, cyclic, 

def emission_maps(model, var, startyr, endyr):
    from pathfinder import pathfinder_var, pr_pathfinder
    
    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'  #This folder needs to be sshfs-ed
    else:
        path = '/trd-project1/' # Betzy
    
    if 'bc' in var:
        variable = 'emibc'
    else:
        variable = 'emiso2'   
    
    emipath = pathfinder_var(model,variable)
    emission = lookup(path+emipath,variable)
    #print(str(emission.time[0]))
    sec_2_yr = 1/(365*24*60*60)
    emission = emission*sec_2_yr*1E12  #gå from sec to yr and from kg to ng
    if 'CNRM' in model:
        emission = emission.sel(time=slice(cftime.DatetimeGregorian(startyr, 1, 1),cftime.DatetimeGregorian(endyr, 1, 1))).mean(dim='time')
    else:
        emission = emission.sel(time=slice(cftime.DatetimeNoLeap(startyr, 1, 1),cftime.DatetimeNoLeap(endyr, 1, 1))).sum(dim='time')
    print(emission)
    plt.figure(figsize=(13,7))
    ax1 = plt.subplot(1,1,1,projection=ccrs.PlateCarree())
    ax1.set_extent ((-180, 180, -20, 90), ccrs.PlateCarree())
    ax1.text(-30,95,model+' '+variable+' avg from '+str(startyr)+' to '+str(endyr)+'')
    #ax1.stock_img()
    ax1.coastlines()
    cs = emission.plot.pcolormesh(ax=ax1,add_colorbar=False,cmap="GnBu",vmin=0, vmax=0.04)#, norm=colors.LogNorm(vmin=emission.min(), vmax=emission.max()))
    #cs = ax1.pcolormesh(emission, cmap="summer")
    CB = plt.colorbar(cs,orientation='horizontal',shrink=0.9) #norm=colors.LogNorm(), cmap='coolwarm'
    print(emission.min(),emission.max())
    CB.set_label('ng m-2 yr-1', fontsize=15)
    plt.savefig('test.png')
    plt.savefig('/cluster/home/krisomos/ice_cores/output/'+model+'_'+variable+'_'+str(startyr)+'-'+str(endyr)+'.png')


def emission_per_region(model,var,area):
    from pathfinder import pathfinder_var, pr_pathfinder
    import regiondefinitions as rd
    reg_info = rd.getregiondefinition(area)

    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'  #This folder needs to be sshfs-ed
    else:
        path = '/trd-project1/' # Betzy
    
    if 'bc' in var:
        variable = 'emibc'
    else:
        variable = 'emiso2'
        
    
    emipath = pathfinder_var(model,variable)
    emission = lookup(path+emipath,variable)
    
    DoNotUse, DoNotUse1, areapath = pr_pathfinder(model)
    areafile = xr.open_dataset(path+areapath)['areacella']
    lonA, lonB, cyclic= regionfixer(area, reg_info)
    
    if cyclic == True:
        # this tests if the region crosses the meridional, and if so makes sure the right area is picked
        # first I create a boolean (True/False) array for the longitude values I'm interested in
        boolelon = (emission.lon.values < lonB) | (emission.lon > lonA)
        newlon = emission.lon.values[boolelon]
    else:
        newlon = emission.sel(lon=slice(lonA,lonB)).lon.values

    
    emission = emission.sel(lat=slice(reg_info['latA'],reg_info['latB']),lon=newlon).groupby('time.year').mean()          # kg m-2 s-1 
    areafile = areafile.sel(lat=slice(reg_info['latA'],reg_info['latB']))                                                 # m2
    areafile = areafile.sel(lon=newlon,method='nearest')                                                                  # m2
    emission_temp = emission*areafile                                                                                     # kg s-1 
    emission_temp = emission_temp.sum(dim='lon').sum(dim='lat')                                                           # kg s-1
    sec_2_yr = 1/(365*24*60*60)                                                                                           # sec to yr constant
    kg_2_tg  = 1.0E-9                                                                                                     # kg  to Tg constant
    emission_tot = emission_temp*(kg_2_tg/sec_2_yr)                                                                       # kg s-1 --> Tg yr-1
                                                          
    outfile = xr.DataArray(emission_tot, name=variable,attrs=dict(units='Tg yr-1'))
    outfile.to_netcdf('/cluster/home/krisomos/ice_cores/output/'+variable+'_'+area+'_'+model+'.nc')
    #print(emission_tot)
    
models =  ['CNRM-ESM2-1','CESM2','GFDL-ESM4','CanESM5','GISS-E2-1-H','GISS-E2-1-G','CESM2-WACCM','NorESM2-LM','INM-CM4-8', 'INM-CM5-0'] #'EC-Earth3-AerChem','MPI-ESM-1-2-HAM', ARE MISSING EMISSIONFILES
#models = ['NorESM2-LM','INM-CM4-8', 'INM-CM5-0']
emission_maps(models[1],'so4', 1960, 1980)

"""
areas = ['CHN','NAM','US','USW','USE','EUR','EA','SA']
for model in models:
    for area in areas:
        emission_per_region(model,'so4',area)
"""