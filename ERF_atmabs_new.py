#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 19:52:22 2021
Make a tableof ERF, atm abs and surface ERF per model per experiment
@author: kristineom
"""
import xarray as xr
import numpy as np
import glob,os
import sys
import re
import warnings
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
else:    
    print("Directory is not empty")




def globalmean(array):
    latitude = array['lat']
    latitude_radians = latitude * np.pi / 180
    weight = np.cos(latitude_radians)
    
    array = array.mean(dim='lon')
    array = (array*weight)/np.sum(weight)
    array = array.sum(dim='lat')     
    #array = array.groupby('time.year').mean()
    
    #go from monthly to yearly data
    monthw = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    monthw = monthw/np.sum(monthw)
    
    #print(len(array.time))
    listing = []
    j=0
    for i in range(0,int(len(array.time)/12)):
        listing.append(float(np.sum((array[j:j+12])*monthw)))
        j = j+12
        #print(j)
    #print(listing)
    
    return listing

def lookup_rad(var, model,exp):
    # This function finds the model data based on path and variable and concatenates
    # it together if needed, then returns one dataarray with the sorted timeseries of the desired variable
    # ----------------------------------
    #print(fullpath)
    list_of_data = []
    #print(model,exp)
    if 'NorESM' in model:
        #print('/home/kristineom/Documents/phdgreier/lifetimes/noresm/CMIP6/*/*/'+model+'/piClim-'+exp+'/r1i1p2*/AERmon/'+var+'/g*/latest/*')
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/noresm/CMIP6/*/*/'+model+'/piClim-'+exp+'/r1i1p2*/Amon/'+var+'/g*/latest/*'):
            #print(file)
            list_of_data.append(file)
    elif 'MPI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data.append(file)
    elif 'GISS' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i1p3f1/Amon/'+var+'/g*/v*/*'):
            list_of_data.append(file)
    elif 'MRI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data.append(file)
    elif 'EC-Earth' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data.append(file)        
    elif 'WACCM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data.append(file)                    
    else:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-'+exp+'/r1i*/Amon/'+var+'/g*/latest/*'):
            list_of_data.append(file)
    
    #print(list_of_data)
    ds =  xr.open_mfdataset(list_of_data, combine='nested', concat_dim='time', chunks={"time":12}, parallel=True)[var]    
    ds = ds.sortby('time')
    ds = globalmean(ds)
    #---- ctrl ----
    list_of_data_ctrl = []
    if 'NorESM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/noresm/CMIP6/*/*/'+model+'/piClim-control/r1i1p2*/Amon/'+var+'/g*/latest/*'):
            #print(file)
            list_of_data_ctrl.append(file)
    elif 'MPI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data_ctrl.append(file)
    elif 'GISS' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i1p3f1/Amon/'+var+'/g*/v*/*'):
            list_of_data_ctrl.append(file)            
    elif 'MRI' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data_ctrl.append(file)
    elif 'EC-Earth' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data_ctrl.append(file)        
    elif 'WACCM' in model:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i*/Amon/'+var+'/g*/v*/*'):
            list_of_data_ctrl.append(file)                    
    else:
        for file in glob.glob('/home/kristineom/Documents/phdgreier/lifetimes/nird/*/*/'+model+'/piClim-control/r1i*/Amon/'+var+'/g*/latest/*'):
            list_of_data_ctrl.append(file)
    
    #print(list_of_data)
    ds_ctrl =  xr.open_mfdataset(list_of_data_ctrl, combine='nested', concat_dim='time', chunks={"time":12}, parallel=True)[var]    
    ds_ctrl = ds_ctrl.sortby('time')
    ds_ctrl = globalmean(ds_ctrl)
    if len(ds) < len(ds_ctrl):
        ds_ctrl = ds_ctrl[0:len(ds)]
    elif len(ds) > len(ds_ctrl):
        ds = ds[0:len(ds_ctrl)]
    #print(len(ds_ctrl),len(ds))
    return ds_ctrl, ds    


def calc_ERFetc_SW(model, experiment):
    
    rsut_ctrl, rsut_exp = lookup_rad('rsut',model,experiment)
    rsdt_ctrl, rsdt_exp = lookup_rad('rsdt',model,experiment)
    rsus_ctrl, rsus_exp = lookup_rad('rsus',model,experiment)
    rsds_ctrl, rsds_exp = lookup_rad('rsds',model,experiment)
    rsuscs_ctrl, rsuscs_exp = lookup_rad('rsuscs',model,experiment)
    rsdscs_ctrl, rsdscs_exp = lookup_rad('rsdscs',model,experiment)
    rsutcs_ctrl, rsutcs_exp = lookup_rad('rsutcs',model,experiment)

    ERF = np.mean((np.absolute(rsdt_exp) - np.absolute(rsut_exp)) - (np.absolute(rsdt_ctrl) - np.absolute(rsut_ctrl)))
    ERF_surf = np.mean((np.absolute(rsds_exp) - np.absolute(rsus_exp)) - (np.absolute(rsds_ctrl) - np.absolute(rsus_ctrl)))
    atm_abs = ERF - ERF_surf
    
    ERFcs = np.mean((np.absolute(rsdt_exp) - np.absolute(rsutcs_exp)) - (np.absolute(rsdt_ctrl) - np.absolute(rsutcs_ctrl)))
    ERF_surfcs = np.mean((np.absolute(rsdscs_exp) - np.absolute(rsuscs_exp)) - (np.absolute(rsdscs_ctrl) - np.absolute(rsuscs_ctrl)))
    atm_abs_cs = ERFcs - ERF_surfcs
    
    return ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abs_cs



def calc_ERFetc_LWSW(model, experiment):
    rsut_ctrl, rsut_exp = lookup_rad('rsut',model,experiment)
    rsdt_ctrl, rsdt_exp = lookup_rad('rsdt',model,experiment)
    rsus_ctrl, rsus_exp = lookup_rad('rsus',model,experiment)
    rsds_ctrl, rsds_exp = lookup_rad('rsds',model,experiment)

    rlut_ctrl, rlut_exp = lookup_rad('rlut',model,experiment)
    rlus_ctrl, rlus_exp = lookup_rad('rlus',model,experiment)
    rlds_ctrl, rlds_exp = lookup_rad('rlds',model,experiment)   
    
    #rsuscs_ctrl, rsuscs_exp = lookup_rad('rsuscs',model,experiment)
    #rsdscs_ctrl, rsdscs_exp = lookup_rad('rsdscs',model,experiment)
    #rsutcs_ctrl, rsutcs_exp = lookup_rad('rsutcs',model,experiment)

    #rluscs_ctrl, rluscs_exp = get_globmeanyrly('rluscs',model,experiment)
    #rldscs_ctrl, rldscs_exp = lookup_rad('rldscs',model,experiment)
    #rlutcs_ctrl, rlutcs_exp = lookup_rad('rlutcs',model,experiment)

    #print(rsdt_ctrl)
    
    # TOA
    rsnt_exp = (np.absolute(rsdt_exp) - np.absolute(rsut_exp))
    rsnt_ctrl = (np.absolute(rsdt_ctrl) - np.absolute(rsut_ctrl))
    rlnt_exp = ( np.absolute(rlut_exp))
    rlnt_ctrl = ( np.absolute(rlut_ctrl))
    # surface
    rsns_exp = (np.absolute(rsds_exp) - np.absolute(rsus_exp))
    rsns_ctrl = (np.absolute(rsds_ctrl) - np.absolute(rsus_ctrl))
    rlns_exp = ( np.absolute(rlds_exp) - np.absolute(rlus_exp))
    rlns_ctrl = (np.absolute(rlds_ctrl) - np.absolute(rlus_ctrl))
    
    #print(len(rsnt_exp), len(rsnt_ctrl), len(rlnt_exp), len(rlnt_ctrl))

    
    ERF = np.mean( (rsnt_exp - rsnt_ctrl) - ( rlnt_exp - rlnt_ctrl)) 
    ERF_surf = np.mean((rsns_exp - rsns_ctrl) - (rlns_exp - rlns_ctrl))
    atm_abs = ERF - ERF_surf
    
    # TOA
    #rsntcs_exp = (np.absolute(rsdt_exp) - np.absolute(rsutcs_exp))
    #rsntcs_ctrl = (np.absolute(rsdt_ctrl) - np.absolute(rsutcs_ctrl))
    #rlntcs_exp = ( np.absolute(rlutcs_exp))
    #rlntcs_ctrl = ( np.absolute(rlutcs_ctrl))
    # surface
    #rsnscs_exp = (np.absolute(rsds_exp) - np.absolute(rsuscs_exp))
    #rsnscs_ctrl = (np.absolute(rsds_ctrl) - np.absolute(rsuscs_ctrl))
    #rlnscs_exp = ( np.absolute(rldscs_exp) - np.absolute(rlus_exp))
    #rlnscs_ctrl = (np.absolute(rldscs_ctrl) - np.absolute(rlus_ctrl))
    
    
    #ERFcs = np.mean( (rsntcs_exp - rsntcs_ctrl) - (rlntcs_exp - rlntcs_ctrl)) 
    #ERF_surfcs = np.mean((rsnscs_exp - rsnscs_ctrl) - (rlnscs_exp - rlnscs_ctrl))
    #atm_abs_cs = ERFcs - ERF_surfcs
    
    #return ERF.values, ERF_surf.values, atm_abs.values, ERFcs.values, ERF_surfcs.values, atm_abs_cs.values
    return ERF, ERF_surf, atm_abs#, ERFcs, ERF_surfcs, atm_abs_cs

def Modellist(model,exp):
    matchlist = []
    pathdir = '/home/kristineom/Documents/phdgreier/ice_cores/new_cmipfolder/'
    for file in glob.glob(pathdir+'ESGF/CMIP6/*/*/*/piClim-'+exp+'/r1i1*/Amon/rsds/*/v*/*'):
        #print(file)
        
        x = re.search(r'(.*[?!_])(.*)_piClim-',file)
        if x == None:
            continue
        else:
            if x.group(2) in matchlist:
                continue
            else:
                matchlist.append(x.group(2))
    
    matchlist1 = []
    for file1 in glob.glob(pathdir+'ESGF/CMIP6/*/*/*/piClim-control/r1i1*/Amon/rsds/*/v*/*'):
        #print(file)
        
        x1 = re.search(r'(.*[?!_])(.*)_piClim-',file1)
        if x1 == None:
            continue
        else:
            if x1.group(2) in matchlist1:
                continue
            else:
                matchlist1.append(x1.group(2))
    combo = list(set(matchlist).intersection(matchlist1))
    return combo

def print_tableinfo_LWSW(modellist,explist):
    outfile = open("/home/kristineom/Documents/phdgreier/lifetimes/ERF_LWSW.txt","w")
    #print(' &  &   ERF &  ERF_surf &AtmAbs& ERF CS& ERF_surf clear sky & AtmAbs CS \n')
    outfile.write('  &  &   ERF &  ERF_surf & AtmAbs & ERF CS & ERF_surf clear sky & AtmAbs CS \n')
    for exp in explist:
        outfile.write(' {0} & & & & & & & \n'.format(exp))
        #matchlist = Modellist(exp)

        print(repr('\textbf{'),exp,'}')
        for model in modellist:
            ERF, ERF_surf, atm_abs = calc_ERFetc_LWSW(model, exp)
            print('&',model,f'  & {ERF:.2f}   &   {ERF_surf:.2f}   &     {atm_abs:.2f}  ')#&      {ERFcs:.2f}&      {ERF_surfcs:.2f}     & {atm_abscs:.2f}  \\')
            outfile.write('& {0} & {1:.2f} & {2:.2f} & {3:.2f}  \\\ \n'.format(model,ERF,ERF_surf,atm_abs))
    outfile.close()
    
def print_tableinfo_SW(explist):
    outfile = open("/home/kristineom/Documents/phdgreier/rsds_models/ERF_SW.txt","w")
    #print('  &  &   ERF &  ERF_surf &AtmAbs& ERF CS& ERF_surf clear sky & AtmAbs CS \n')
    outfile.write('  &  &   ERF &  ERF_surf & AtmAbs & ERF CS & ERF_surf clear sky & AtmAbs CS \n')
    for i in range(len(explist)):
        outfile.write(' {0} & & & & & & & \n'.format(explist[i]))
        matchlist = Modellist(explist[i])
        print(repr('\textbf{'),explist[i],'}')
        for j in range(len(matchlist)):
            if 'NorESM' in matchlist[j]:
                print('nei')
            else:
                ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abscs = calc_ERFetc_SW(matchlist[j], explist[i])
                outfile.write('& {0} & {1:.2f} & {2:.2f} & {3:.2f} & {4:.2f} & {5:.2f} & {6:.2f} \\\ \n'.format(matchlist[j],ERF,ERF_surf,atm_abs, ERFcs, ERF_surfcs, atm_abscs))
                print('&',matchlist[j],f'  & {ERF:.2f}   &   {ERF_surf:.2f}   &     {atm_abs:.2f}   &      {ERFcs:.2f}&      {ERF_surfcs:.2f}     & {atm_abscs:.2f}  \\')
    outfile.close()


#explist = ['4xCO2',
#explist = ['2xVOC','2xDMS','2xss','2xdust','ghg','BC','aer','OC','SO2','NTCF']
explist = ['aer','BC','SO2']
models = ['MRI-ESM2-0','GISS-E2-1-G','CNRM-ESM2-1','NorESM2-LM','MIROC6'] #,'GFDL-ESM4'
# 'MPI-ESM-1-2-HAM' mangler en del variabler på nird: rsdt, rsus, rsds, rlus, rlds
# 'MRI-ESM2-0' har alt (ikke sjekket clearsky)
# GISS is fine as long as u use r1i1p3f1 only!!
# CNRM is fine
# MIROC6 is fine
# GFDL is fine for aer

#models =  ['MPI-ESM-1-2-HAM','CESM2','CESM2-WACCM','MRI-ESM2-0','GISS-E2-1-H','GISS-E2-1-G', 'MIROC6',
#       'EC-Earth3-AerChem','GFDL-ESM4','CNRM-ESM2-1']#,'NorESM2-LM']
#ERF_testing( 'MRI-ESM2-0', explist[0])
print_tableinfo_LWSW(models,['BC'])

#print_tableinfo_LWSW(models,['aer','BC','SO2'])

