
import pandas as pd
import os,glob,sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import matplotlib.colors as colors
import cartopy.crs as ccrs
from dask.diagnostics import ProgressBar
import geonum.atmosphere as atm    # used to calculate atmospheric quanteties
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid
warnings.simplefilter("ignore") 
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

if not os.listdir('/home/kristineom/Documents/phdgreier/lifetimes/nird'):
    print("Directory nird is empty")
    print("sshfs krisomos@login.nird.sigma2.no:/projects/NS9252K/ESGF/CMIP6/ nird/")
    sys.exit()
elif not os.listdir('/home/kristineom/Documents/phdgreier/lifetimes/noresm'):
    print('Directory noresm is empty')
    print("sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ noresm/")
    sys.exit()
elif not os.listdir('/home/kristineom/Documents/phdgreier/ice_cores/betzy/'):
    print('betzy in icecorefolder not mounted')
    print('sshfs krisomos@betzy.sigma2.no:/trd-project1/ betzy/')
    sys.exit()
else:    
    print("Mounted directories on point")

colors = {
    'CanESM5': '#377eb8',
    'CESM2':   '#984ea3',
    'CESM2-WACCM': '#f781bf',
    'GFDL-ESM4': '#a65628',
    'CNRM-ESM2-1': '#999999',
    'GISS-E2-1-H': '#bcbd22',
    'GISS-E2-1-G': '#dede00',
    'NorESM2-LM': '#4daf4a',
    'MIROC6': '#ff7f00',
    'MRI-ESM2-0': '#e41a1c',
    'EC-Earth3-AerChem': '#6c49da',
    'MPI-ESM-1-2-HAM': '#dbc2ba',
}

markers = {
    'CanESM5': 'o',
    'CESM2': 'D', 
    'CESM2-WACCM': 'v',
    'GFDL-ESM4': '^',
    'CNRM-ESM2-1': '^',
    'GISS-E2-1-H': '*',
    'GISS-E2-1-G': '>',
    'NorESM2-LM': '<',
    'MIROC6': 's',
    'MRI-ESM2-0': 'o',
    'EC-Earth3-AerChem': 'D',
    'MPI-ESM-1-2-HAM': '*',
}


def lookup(fullpath, var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    list_of_data = []
    for file in glob.glob(fullpath):
        list_of_data.append(file)
        
    ds =  xr.open_mfdataset(list_of_data, combine='nested', concat_dim='time', chunks={"time":12}, parallel=True)[var]    
    return ds.sortby('time')

def historical_lifetime(models,variable):
    for model in models:
        lifetimepath = '/home/kristineom/Documents/phdgreier/ice_cores/data/lifetime'+variable+'_'+model+'.nc'
        lifetimes = xr.open_dataset(lifetimepath)['__xarray_dataarray_variable__']
        start = lifetimes[0:15].mean().values
        end = lifetimes[-15:].mean().values
        change = end - start
        np.set_printoptions(precision=1)
        print(model,'&',np.around(start,1),'&', np.around(end,1),'&', np.around(change,1), '\\')


def hist_wetdry_ratio(models):
    from pathfinder import pathfinder, pr_pathfinder
    from icecore_ratios import chunks, yearavg
    fig, ax1 = plt.subplots()
    for model in models:
        histwet, histdry, ctrlwet, ctrldry = pathfinder(model,'bc')
        histprpath, ctrlprpath, areafile  = pr_pathfinder(model)
        area = xr.open_dataset(areafile)['areacella']
        wet = lookup(histwet,'wetbc')
        dry = lookup(histdry,'drybc')
        pr = lookup(histprpath,'pr')
        #print(pr)
        #print(area)

        wet = np.absolute(wet)*area
        dry = np.absolute(dry)*area
        if 'MRI' in model:
            areapr = xr.open_dataset('/home/kristineom/Documents/phdgreier/lifetimes/nird/CMIP/MRI/MRI-ESM2-0/historical/r1i1p1f1/fx/areacella/gn/v20190603/areacella_fx_MRI-ESM2-0_historical_r1i1p1f1_gn.nc')['areacella']
            pr = pr*areapr
        else:
            pr = pr*area
        wet = wet.sum(['lon','lat'])
        dry = dry.sum(['lon','lat'])
        pr = pr.sum(['lon','lat'])

        ratio = dry/wet
        ratio = ratio.groupby('time.year').mean()
        pr = pr.groupby('time.year').mean()

        #print(model,ratio)
        datalist, yearlist = yearavg(ratio, ratio.year,10)
        prlist, pryearlist = yearavg(pr, pr.year, 10)

        #ax2 = ax1.twinx()
        #ax1.plot(yearlist,datalist, color=colors[model])
        prstart = prlist[0]
        prlist[:] = [number - prstart for number in prlist]
        ax1.plot(pryearlist, prlist, '--',color=colors[model])
        plt.savefig('/home/kristineom/Documents/phdgreier/lifetimes/images/precip.png')
    plt.show()



models =  ['MPI-ESM-1-2-HAM','CESM2','CESM2-WACCM','MRI-ESM2-0','GISS-E2-1-H','GISS-E2-1-G','NorESM2-LM', 'MIROC6',
           'EC-Earth3-AerChem','GFDL-ESM4','CNRM-ESM2-1']

#models = ['MPI-ESM-1-2-HAM', 'MRI-ESM2-0']#'NorESM2-LM','CESM2',
hist_wetdry_ratio(models)
#historical_lifetime(models,'bc')