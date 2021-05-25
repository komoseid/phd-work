import pandas as pd
import numpy as np
import sys,os,glob
import xarray as xr
import warnings
warnings.simplefilter("ignore")
# needed for betzy
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

def icecore_info():
    #### ICE CORE = UPPER FREEMONT GLACIER ####
    obs = pd.read_csv('/cluster/home/krisomos/example/Upper_freemont_glacier.csv')
    iceyear = obs['Mid_Year'][::-1]
    icedata = obs['BC_ng/g'][::-1].values
    icelat = obs['lat'][0]
    icelon = obs['lon'][0]+360   # xarray is dumb and doesnt understand negative longitude values - exception function should be used in case of other ice cores
    return icedata, iceyear, icelat, icelon



def lookup(fullpath, var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    list_of_data = []
    for file in glob.glob(fullpath+var+'_*.nc'):
        print(file)
        opendata = xr.open_dataset(file)[var]
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

def make_concentration(icelat,icelon):
    path = '/cluster/home/krisomos/example/'  
    wetbc_tot = lookup(path,'wetbc')         # kg/m2/s
    drybc_tot = lookup(path,'drybc')         # kg/m2/s
    prect_tot = lookup(path,'pr')            # kg/m2/s
    area_tot  = xr.open_dataset(path+'areacella_fx_CanESM5_historical_r1i1p1f1_gn.nc')['areacella']  # m2


    wetbc = wetbc_tot.sel(lat=icelat,lon=icelon,method='nearest').groupby('time.year').mean()  # kg/m2/s
    drybc = drybc_tot.sel(lat=icelat,lon=icelon,method='nearest').groupby('time.year').mean()  # kg/m2/s
    prect = prect_tot.sel(lat=icelat,lon=icelon,method='nearest').groupby('time.year').mean()  # kg/m2/s
    area  = area_tot.sel(lat=icelat,lon=icelon,method='nearest')                               # m2

    # Fine - I don't really need to do this but I often look at prec or dep alone so why not just have it there
    depbc = (np.absolute(wetbc) + np.absolute(drybc))*area.values*(365*24*60*60)               # kg
    prec  = prect*area.values*(365*24*60*60)                                                   # kg

    conc = (depbc/prec)*(1E12/1E3)                                                             # kg/kg --> ng/g

    return conc

ice_conc, iceyear, icelat, icelon = icecore_info()
model_conc = make_concentration(icelat,icelon)
print(ice_conc,model_conc)