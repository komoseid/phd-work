#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:54:13 2021
To run this script you need to mount a folder for the noresmdata that is not already mounted on betzy
sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ noresmdata/
This script shall open and read the "new" concentration spreadsheets I got from Joe McConnell and Anja Eichler
ppb = ug/l = ng/g
@author: kristineom
"""
import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import warnings
warnings.simplefilter("ignore")
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

def find_3x3matrix(var_ctrl, lati, long,arealook=False):

    #find closest grid point
    closest = var_ctrl.sel(lat=lati,lon=long,method='nearest')
    #find indices of closest grid point
    index = np.where((var_ctrl.lat == closest.lat.values) & (var_ctrl.lon == closest.lon.values))      
    latind = index[0]
    lonind = index[1]   
    
    #find surrounding grid points
    point11 = var_ctrl.isel(lat=latind+1,lon=lonind+1)
    point10 = var_ctrl.isel(lat=latind+1,lon=lonind)
    point1_1 = var_ctrl.isel(lat=latind+1,lon=lonind-1)

    point_11 = var_ctrl.isel(lat=latind-1,lon=lonind+1)
    point_10 = var_ctrl.isel(lat=latind-1,lon=lonind)
    point_1_1 = var_ctrl.isel(lat=latind-1,lon=lonind-1)
    
    point01 = var_ctrl.isel(lat=latind,lon=lonind+1)
    point00 = var_ctrl.isel(lat=latind,lon=lonind)    #techniqally this is the same as closest, but like do include it here for clarity
    point0_1 = var_ctrl.isel(lat=latind,lon=lonind-1)
    
    if arealook==True:
    # This is for when you are calculating the area of the gridpoints in question
        meanval = (point11.squeeze()+point10.squeeze()+point1_1.squeeze()+point_11.squeeze()+point_10.squeeze()+point_1_1.squeeze()+point01.squeeze()+point00.squeeze()+point0_1.squeeze())
        outfile = meanval
    else:
        point11 = point11.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point10 = point10.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point1_1 = point1_1.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
    
        point_11 = point_11.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point_10 = point_10.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point_1_1 =point_1_1.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        
        point01 = point01.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point00 = point00.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        point0_1 =point0_1.groupby('time.year').mean().squeeze()#*(1E6/3.17098E-8)
        
        #meanval = (point11+point10+point1_1+point_11+point_10+point_1_1+point01+point00+point0_1)/9 
        meanval = (point11+point10+point1_1+point_11+point_10+point_1_1+point01+point00+point0_1)  #ONLY USE THIS IF YOU ARE DOING ug/g
  
        outfile = xr.DataArray(meanval, coords=[point11.year],dims="year")
    return outfile

"""
# THIS FUNCTIONS DOES NOT WORK AS NEEDED YET - FIX LATER
def dms2deg(coord):
    import re
    regex = re.compile("(\d+)°(\d+)'(?:(\d+)'')?([NESW])")
    #lat = "45°55'55''N"
    print(regex.match(coord).groups())
    #lat = '''51°36'9.18"N'''
    #deg, minutes, seconds, direction =  regex.match(coord).groups()
    decimalcoord = (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)
    return decimalcoord
"""

def find_eichler_icecore(name, var):
    # load data from ice core spreadsheet sent from Anja Eichler,
    # this includes Colle Gnifetti, Belukha, Lomonosovfonna and Illimani
    obs = pd.ExcelFile('/cluster/home/krisomos/ice_cores/data/Sulfat_BC_ice_cores_Eichler.xlsx')
    ice_latlon = pd.read_excel(obs, name)
    lat = ice_latlon[name].iloc[0].split(',')[0]
    lon = ice_latlon[name].iloc[0].split(',')[1]
    print(lon)
    #newlat = dms2deg(lat)
    #newlon = dms2deg(lon)
    #print(lon, newlon)

    ice_data = pd.read_excel(obs, name, skiprows=2)
    if 'so' in var:
        ice = ice_data['total SO42- (ppb = mg/l)']
    else:
        ice = ice_data['BC (ppb)']
    ice_year = ice_data.iloc[:,0]

    #print(ice)

def find_mcconnell_icecore(name, var):
    # 
    #
    # Ex: data, year, lat, lon = find_mcconnell_icecore('Ngreen', 's')
    #--------------------------------------------------------------------
    obs = pd.ExcelFile('/cluster/home/krisomos/ice_cores/data/Greenland_data_for_Kine_051021.xlsx')
    ice = pd.read_excel(obs,'Concentration_All_1750_2012')
    icename = pd.read_excel(obs,'Core Stats')
    
    icelat = []
    icelon = []
    ice_data = []
    if "Sgreen" in name:
        namelist = ['ACT2', 'ACT11D', 'D4', 'Summit2010'] 
    elif "Ngreen" in name:
        namelist= ['NGT_B19', 'Tunu2013', 'NEEM_2011_S1',  'Humboldt']
    else:
        namelist=[name]

    if 'bc' in var:
        newnames = [s + '_BC_ng_g' for s in namelist]
    elif 's' in var:
        newnames = [s + '_nssS_ng_g' for s in namelist]


    for i in range(len(namelist)): 
        hei = icename[icename['Core'].isin([namelist[i]])]
        ice_lat = hei['Lat'].values[0]
    
        ice_lon = hei['Lon'].values[0]
        if ice_lon < 0:
            ice_lon = ice_lon+360
        else:
            print(ice_lon)
        
        icelat.append(ice_lat)
        icelon.append(ice_lon)

        icedata = ice[newnames[i]].values
        ice_data.append(icedata)
    
    
    ice_year = ice['Mid Year'].values
    
    ice_data = np.nanmean(ice_data,axis=0) #Note that by using nanmean we ignore the icecores with nan values, so some years have a mean based on fewer sites

    return ice_data[::-1], ice_year[::-1], icelat, icelon
    
def lookup(fullpath, var):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    list_of_data = []
    for file in glob.glob(fullpath):
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

def model_concentration_timeseries(model, var, lati, longi):

    from pathfinder import pathfinder
    from pathfinder import pr_pathfinder

    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'  #This folder needs to be sshfs-ed
    else:
        path = '/trd-project1/' # Betzy

    histwetpath, histdrypath, ctrlwetpath, ctrldrypath = pathfinder(model,var)
    histprpath, ctrlprpath, areafile                   = pr_pathfinder(model)
    wet = 'wet'+var
    dry = 'dry'+var
    
    # Create one sorted timeseries per variable in Q 
    vaat      = lookup(path+histwetpath,wet)
    #vaat_ctrl = lookup(path+ctrlwetpath,wet)
    torr      = lookup(path+histdrypath,dry)
    #torr_ctrl = lookup(path+ctrldrypath,dry)
    pr        = lookup(path+histprpath,'pr')
    #pr_ctrl   = lookup(path+ctrlprpath,'pr')

    area      = xr.open_dataset(path+areafile)['areacella']

    # Calculate the concentration from the historical experiment and change unit to kg
    area = find_3x3matrix(area,lati,longi,True)                 # m2

    torr = find_3x3matrix(torr, lati,longi)                     # kg m-2 s-1
    torr = torr*area.values*(365*24*60*60)                      # kg

    vaat = find_3x3matrix(vaat, lati,longi)                     # kg m-2 s-1
    vaat = vaat*area.values*(365*24*60*60)                      # kg

    prec = find_3x3matrix(pr,lati,longi)                        # kg m-2 s-1
    acc = prec
    prec = prec*area.values*(365*24*60*60)                      # kg

    tot_dep = np.absolute(torr) + np.absolute(vaat)             # kg
    conc = (tot_dep/prec)*(1E12/1E3)                            # kg/kg --> ng/g

    """
    # Same for piControl
    torr_ctrl = find_3x3matrix(torr_ctrl, lati,longi)           # kg m-2 s-1
    torr_ctrl = torr_ctrl*area.values*(365*24*60*60)            # kg

    vaat_ctrl = find_3x3matrix(vaat_ctrl, lati,longi)           # kg m-2 s-1
    vaat_ctrl = vaat_ctrl*area.values*(365*24*60*60)            # kg

    prec_ctrl = find_3x3matrix(pr_ctrl,lati,longi)              # kg m-2 s-1
    prec_ctrl = prec_ctrl*area.values*(365*24*60*60)            # kg

    tot_dep_ctrl = np.absolute(torr_ctrl) + np.absolute(vaat_ctrl)    # kg
    conc_ctrl = (tot_dep_ctrl/prec_ctrl)*(1E12/1E3)                   # kg/kg --> ng/g
    conc_ctrl = np.mean(conc_ctrl)

    # Find concentration anomaly
    dConc = conc - conc_ctrl

    out = xr.DataArray(dConc,name='conc_anomaly')
    out['conc_absolute'] = xr.DataArray(conc)
    out['conc_ctrl'] = conc_ctrl
    print(type(out))
    print(out)
    """
    out = xr.DataArray(conc, name='Conc_Absolute')
    return out

def acc_rate(model, lati, longi):
    # This function calculates the accumulation rates per ice core site
    # This is an important first step to check if models are way off on the local "climate" of a site.
    # ----------------------------------------------
    from pathfinder import pathfinder
    from pathfinder import pr_pathfinder

    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'  #This folder needs to be sshfs-ed as described at top of script
    else:
        path = '/trd-project1/' # Betzy

    histprpath, ctrlprpath, areafile                   = pr_pathfinder(model)
    pr        = lookup(path+histprpath,'pr')

    # Calculate the accumulation rate
    prec = find_3x3matrix(pr,lati,longi)                        # kg m-2 s-1
    acc = prec

    out = xr.DataArray(acc, name='Acc_Absolute')
    return out

def write_netcdf_prec(name):
    # Write the netcdffile that contains the accumulation rates
    # ------------------------------
    data, year, lat, lon = find_mcconnell_icecore(name,'bc')
    models =  ['CNRM-ESM2-1','CESM2','GFDL-ESM4','CanESM5','GISS-E2-1-H','GISS-E2-1-G','CESM2-WACCM','EC-Earth3-AerChem'] #'NorESM2-LM','MPI-ESM-1-2-HAM','INM-CM4-8', 'INM-CM5-0',
    
    for j in range(len(models)):
        if len(lat)>1:
            outlist = []
            for i in range(len(lat)):
                outfile = acc_rate(models[j],lat[i],lon[i])
                outlist.append(outfile.values)

            outfile = xr.DataArray(np.mean(outlist,axis=0), name='Acc_Absolute')
            print(outfile)
        else:
            outfile = acc_rate(models[j],lat,lon)

        outfile.to_netcdf('/cluster/home/krisomos/ice_cores/output/prec_'+models[j]+'_'+name+'_acc.nc')


def write_netcdf(name, var):
    # This function writes a netcdffile per model for the area and variable given. 
    # ----------------------------------------------------------------------------
    data, year, lat, lon = find_mcconnell_icecore(name,var)
    models =  ['CNRM-ESM2-1','CESM2','GFDL-ESM4','CanESM5','GISS-E2-1-H','GISS-E2-1-G','CESM2-WACCM','EC-Earth3-AerChem'] #'NorESM2-LM','MPI-ESM-1-2-HAM','INM-CM4-8', 'INM-CM5-0',
    
    for j in range(len(models)):
        if len(lat)>1:
            outlist = []
            for i in range(len(lat)):
                outfile = model_concentration_timeseries(models[j],var,lat[i],lon[i])
                outlist.append(outfile.values)
            #print(outlist)
            outfile = xr.DataArray(np.mean(outlist,axis=0), name='Conc_Absolute')

            print(outfile)
        else:
            outfile = model_concentration_timeseries(models[j],var,lat,lon)

        outfile.to_netcdf('/cluster/home/krisomos/ice_cores/output/'+var+'_'+models[j]+'_'+name+'_conc.nc')

areas = ['Ngreen','Sgreen','ACT11D','ACT2','NGT_B19','Tunu2013','NEEM_2011_S1','Humboldt','Summit2010','D4']
for k in range(len(areas)):
    #write_netcdf_prec(areas[k])
    write_netcdf(areas[k],'so4')
    write_netcdf(areas[k],'bc')
