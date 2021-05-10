#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:11:14 2021
testing new paths to stop using scratchmaybe make a pathfunction 
sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ noresmdata/
@author: kristineom
"""

import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys 
from pathfinder import pathfinder
import warnings
warnings.simplefilter("ignore") 
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

def make_anomalies(model, var, lati, long):
    seq_list = []
    list1 = []
    if 'NorESM' in model:
        path = '/cluster/home/krisomos/noresmdata/'
    else:
        path = '/trd-project1/' # THIS IS WHERE THE PATH CHANGES
    histwetpath, histdrypath, ctrlwetpath, ctrldrypath = pathfinder(model,var)
    wet = 'wet'+var
    dry = 'dry'+var

    # ----------- historical -----------------------
    for file in glob.glob(path+histwetpath):
        print(file)
        vaat = xr.open_dataset(file)[wet]
        seq_list.append(vaat)
    if len(seq_list) > 1:
        print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(seq_list,dim='time')
        vaat = concatted.sortby('time')
    elif len(seq_list)==0:
        print('NO MATCHES FOR THIS MODEL: ',model)
        sys.exit()
    else:
        vaat = seq_list[0]
        

    for file1 in glob.glob(path+histdrypath):
        #print(file1)
        torr = xr.open_dataset(file1)[dry]
        list1.append(torr)
    if len(list1) > 1:
        print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(list1,dim='time')
        torr = concatted.sortby('time')
    elif len(list1)==0:
        print('NO MATCHES FOR THIS MODEL: ',model)
        sys.exit()
    else:
        torr = list1[0]
        
    #------------- PiControl --------------------
    list3 = []
    for file3 in glob.glob(path+ctrlwetpath):
        #print(file3)
        vaat_ctrl = xr.open_dataset(file3)[wet]
        list3.append(vaat_ctrl)
    if len(list3) > 1:
        print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(list3,dim='time')
        vaat_ctrl = concatted.sortby('time')
    elif len(list3)==0:
        print('NO MATCHES FOR THIS MODEL: ',model)
        sys.exit()
    else:
        vaat_ctrl = list3[0]
    vaat_ctrl = vaat_ctrl.groupby('time.month').mean('time')        # create climatology
    
    list4 = []
    for file4 in glob.glob(path+ctrldrypath):
        #print(file4)
        torr_ctrl = xr.open_dataset(file4)[dry]
        list4.append(torr_ctrl)
    if len(list4) > 1:
        print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(list4,dim='time')
        torr_ctrl = concatted.sortby('time')
    elif len(list4)==0:
        print('NO MATCHES FOR THIS MODEL: ',model)
        sys.exit()
    else:
        torr_ctrl = list4[0]
    torr_ctrl = torr_ctrl.groupby('time.month').mean('time')        # create climatology

    # -------------------------------------------------------------------
    vaat = vaat.groupby('time.month') - vaat_ctrl   # create anomaly
    torr = torr.groupby('time.month') - torr_ctrl   #create anomaly
        
    torr = torr.sel(lat=lati,lon=long,method='nearest') #  "kg m-2 s-1" 
    vaat = vaat.sel(lat=lati,lon=long,method='nearest') #  "kg m-2 s-1" 

        
    #I want mg/m2/yr so i need to multiply with 1000000/3.1688E-8
    torr = torr.groupby('time.year').mean()*(1E6/3.17098E-8)
    vaat = vaat.groupby('time.year').mean()*(1E6/3.17098E-8)
        

    depo = np.absolute(torr)+ np.absolute(vaat)  # mg/m2/yr
    return depo

make_anomalies('NorESM2-LM','so4',45,45)
