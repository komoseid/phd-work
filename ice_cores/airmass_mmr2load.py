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
    print(fullpath)
    for file in glob.glob(fullpath):
        print(file)
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


def create_loads(model, var):
    from pathfinder import pathfinder_var, pr_pathfinder
    
    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'  #This folder needs to be sshfs-ed as described at top of script
    else:
        path = '/trd-project1/' # Betzy
    
    
    mmrpath = pathfinder_var(model,'mmr'+var)
    print(mmrpath)
    mmr = lookup(path+mmrpath,'mmr'+var)
    
    airmasspath = pathfinder_var(model,'airmass')
    airmass = lookup(path+airmasspath,'airmass')
    

    #print(mmr)
    #print(airmass)
    #hey = mmr*airmass
    #print(hey)
    print(airmass*mmr)
    
create_loads('CESM2','so4')