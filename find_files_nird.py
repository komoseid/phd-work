#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 14:51:54 2021
sshfs krisomos@login.nird.sigma2.no:/projects/NS9252K/ESGF/CMIP6/ nird/
sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ noresm/
This script finds models and piclim experiments as the user iputs and calculates and prints the lifetime of BC for these models and experiments
@author: kristineom
"""
import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import geonum.atmosphere as atm
import warnings
from dask.diagnostics import ProgressBar
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
    print("Directory is not empty")

def lookup(model,exp,var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    #print(fullpath)
    list_of_data = []
    if 'NorESM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/noresm/CMIP6/*/*/'+model+'/piClim-'+exp+'/r1i1p2*/AERmon/'+var+'/g*/latest/*'):
            #print(file)
            list_of_data.append(file)
    elif 'MPI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            list_of_data.append(file)
    elif 'MRI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            list_of_data.append(file)
    elif 'EC-Earth' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            list_of_data.append(file)        
    elif 'WACCM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            list_of_data.append(file)                    
    else:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/latest/*'):
            list_of_data.append(file)
    
    #print(list_of_data)
    ds =  xr.open_mfdataset(list_of_data, combine='nested', concat_dim='time', chunks={"time":12}, parallel=True)[var]    
    return ds.sortby('time')

#lookup('NorESM2-LM','control','wetbc')

def lookup_mmr(model,exp,var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    list_of_data = []
    #print(fullpath)
    if 'NorESM' in model:
        fullpath = 'noresm/CMIP6/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/latest/*'
    elif 'MPI' in model:
        fullpath = '/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'
    elif 'MRI' in model:
        fullpath = '/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'
    elif 'EC-Earth' in model:      
        fullpath = '/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'
    elif 'WACCM' in model:
        fullpath= '/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'
    else:
        fullpath='nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/latest/*'
        
    for file in glob.glob(fullpath):
        #print(file)
        #opendata = xr.open_dataset(file,decode_times=True, use_cftime=True)[var]
        list_of_data.append(file)
    #print(list_of_data)
    ds =  xr.open_mfdataset(list_of_data, combine='nested', concat_dim='time', chunks={"time":3}, parallel=True)
    #print(ds)
    # Make sure the naming is consistent
    if 'lev_bounds' in ds.variables:
        ds = ds.rename({'lev_bounds':'lev_bnds'})
    if 'nbnd' in ds.dims:
        ds = ds.rename({'nbnd':'bnds'})

    return ds.sortby('time')

def makepath(model,exp,var):
    if 'NorESM' in model:
        for file in glob.glob('noresm/CMIP6/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/latest/*'):
            #print(file)
            return file
    elif 'MPI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            return file
    elif 'MRI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            return file
    elif 'EC-Earth' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            return file
    elif 'WACCM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/v*/*'):
            return file                                
    else:
        for file in glob.glob('nird/*/*/'+model+'/piClim-'+exp+'/r1i*/AERmon/'+var+'/g*/latest/*'):
            #print(file)
            return file

#makepath('NorESM2-LM','control','wetbc')

def make_load_special(model,exp): # 'EC-Earth3-AerChem','CNRM-ESM2-1','MPI-ESM-1-2-HAM' ,'GISS-E2-1-H',  'MRI-ESM2-0','GISS-E2-1-G'
    
    #mmrpath = makepath(model,exp,'mmrbc')
    ds = lookup_mmr(model,exp,'mmrbc')
    #print((ds.bnds))
    # compute concentration
    if "EC-Earth" in model:
        pressure = ds.ap + ds.b*ds.ps
        #area = area_from_bnds(ds)
    elif "MPI" in model:
        pressure = ds.ap + ds.b*ds.ps
    elif "CNRM" in model:
        pressure = ds.ap + ds.b*ds.ps
    else:
        pressure = ds.a*ds.p0+ds.b*ds.ps
    altitude = atm.pressure2altitude(pressure, lat=ds.lat)
    temperature = atm.temperature(altitude)
    density = atm.density(altitude, temperature, lat=ds.lat)/1E3 #this func returns in g/m3 so you need to divide by 1E3 to get kg/m3
    concentration = ds['mmrbc']*density 
    #print(concentration.sum(['lev','lat','lon'])[0:10].values)
    #print(model)

    # compute layer thickness
    if "EC-Earth" in model:
        pressure_bounds = ds.ap_bnds + ds.b_bnds*ds.ps
    elif "MPI" in model:
        pressure_bounds = ds.ap_bnds + ds.b_bnds*ds.ps
    elif "CNRM" in model:
        # CNRM has the wrong shape for its bounds making the layer thickness far to great, therefore a reshaping is needed
        new_b_bnds_temp = np.reshape(ds.b_bnds.values,(len(ds.time),len(ds.lev),len(ds.bnds)))
        new_b_bnds = xr.DataArray(data=new_b_bnds_temp,dims=['time','lev','bnds'],coords=dict(time=ds.time,lev=ds.lev,bnds=ds.bnds))

        new_ap_bnds_temp = np.reshape(ds.ap_bnds.values,(len(ds.time),len(ds.lev),len(ds.bnds)))
        new_ap_bnds = xr.DataArray(data=new_ap_bnds_temp,dims=['time','lev','bnds'],coords=dict(time=ds.time,lev=ds.lev,bnds=ds.bnds))        
        
        pressure_bounds = new_ap_bnds + new_b_bnds*ds.ps
    else:
        pressure_bounds = ds.a_bnds*ds.p0+ds.b_bnds*ds.ps
    
    altitude_bounds = atm.pressure2altitude(pressure_bounds)
    dz = altitude_bounds.diff('bnds')     

    
    # compute load
    load = (dz*concentration).groupby('time.year').mean().squeeze()
    #print(load.sum(['lev','lat','lon'])[100:110].values)
    return load

#make_load_special('CNRM-ESM2-1','control')

def make_load(model,exp):
    #mmrpath = makepath(model,exp,'mmrbc')
    mmr = lookup(model,exp,'mmrbc')
    #print(mmr.sum(['lev','lon','lat']).groupby('time.year').mean())
    
    #airmasspath = makepath(model,exp,'airmass')
    airmass = lookup(model,exp,'airmass')
    #if 'NorESM' in model:
    #    airmass['time'] = mmr.time
    burden = mmr*airmass   #kg/kg * kg/m2 = kg/m2
    burden = burden.groupby('time.year').mean()
    return burden

#make_load('NorESM2-LM','control')
    
#models =  ['MPI-ESM-1-2-HAM','CESM2','CESM2-WACCM','MRI-ESM2-0','GISS-E2-1-H','GISS-E2-1-G', 'MIROC6',
#       'EC-Earth3-AerChem','GFDL-ESM4','CNRM-ESM2-1']#,'NorESM2-LM']
models = ['GFDL-ESM4']
#exp = ['2xVOC','2xDMS','BC','SO2','2xfire','VOC','aer']#'control',
exp = ['BC']#, '2xDMS','BC','SO2','VOC']#

ov = {}

for experi in exp:
    for model in models:
        #print(exp,model)
        out = makepath(model,experi,'wetbc')
        if out == None:
            continue
        else:
            out1 = makepath(model,experi,'drybc')
            if out1 == None:
                continue
            else: 
                ov.setdefault(experi,[]).append(model)
                print('yay '+model+' has both dry and wet bc in '+experi)

print(ov)

for exp, models in ov.items():
    for model in models:

        print(model,exp)        
        from pathfinder import pathfinder, pr_pathfinder
        histprpath, ctrlprpath, areafile  = pr_pathfinder(model)
        area = xr.open_dataset(areafile)['areacella']
        area = area.sel(lat=slice(0,90))
        #wetpath = makepath(model,exp,'wetbc')
        dry = lookup(model,exp,'drybc')
        wet = lookup(model,exp,'wetbc')
        #drypath = makepath(model,exp,'drybc')
        
        tot_dep = np.absolute(wet.groupby('time.year').mean()) + np.absolute(dry.groupby('time.year').mean())
        tot_dep = tot_dep.sel(lat=slice(0,90))
        dep = tot_dep*area # kg per second
        dep = dep.sum(['lon','lat']) # kg per second        
        
        
        if 'GISS' in model:
            load = make_load_special(model,exp)
        elif 'CNRM' in model:
            load = make_load_special(model,exp)
        elif 'MPI' in model:
            load = make_load_special(model,exp)
        elif 'MRI' in model:
            load = make_load_special(model,exp)
        else:
            load = make_load(model,exp)

        load = load.sum(dim='lev')  #kg / m2
        load= load.sel(lat=slice(0,90))
        load = load*area      # kg
        load = load.sum(['lon','lat'])  # kg
        
        
        #print('load: ',load.shape)
        #print('dep: ',dep.shape)
        lifetime_in_days = (load/dep) /(60*60*24)
        print(lifetime_in_days.mean(dim='year').values)
        #drypath = makepath(value,key,'drybc')
        #loadpath = makepath(value,key,'mmrbc')
        