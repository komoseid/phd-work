#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 17:54:13 2021
sshfs krisomos@login.nird.sigma2.no:/scratch/krisomos/100121/ scratch/
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



#print(obs[['Site/Core','Latitude, N','Longitude, E']])

#oldnames = obs['Site/Core']
#names = [x for x in oldnames if str(x) != 'nan']

def find_icecore(name):
    obs = pd.read_csv('/home/kristineom/Documents/phdgreier/ice_cores/data/nssS_data_for_MShulz.csv')

    
    hei = obs[obs['Site/Core'].isin([name])]
    ice_lat = hei['Latitude, N'].values[0]
    ice_lat = float(ice_lat.replace(',','.'))

    ice_lon = hei['Longitude, E'].values[0]
    ice_lon = ice_lon.replace(',','.')
    ice_lon = float(ice_lon.replace('−','-'))
    if ice_lon < 0:
        ice_lon = ice_lon+360
    else:
        print(ice_lon)
    
    ice_year = obs['Mid_Year'].values
    ice_year = [float(item.replace(",", ".")) for item in ice_year]
    
    ice_data = obs[name]

    return ice_data[::-1], ice_year[::-1], ice_lat, ice_lon

def find_icecore_greenland(name):
    obs = pd.read_csv('/home/kristineom/Documents/phdgreier/ice_cores/data/nssS_data_for_MShulz.csv')
    icelat = []
    icelon = []
    if "Sgreen" in name:
        namelist = ['ACT2', 'ACT3', 'D4', 'D5', 'McBales', 'Summit_2010'] #McBales and summit same location (looks like one dot on map)
    elif "Ngreen" in name:
        namelist= ['NGT_B19', 'Tunu13', 'NEEM_2011_S1', 'NEEMS3',  'Humboldt'] #NEEM same location (looks like one dot on map)

    for i in range(len(namelist)): 
        hei = obs[obs['Site/Core'].isin([namelist[i]])]
        ice_lat = hei['Latitude, N'].values[0]
        ice_lat = float(ice_lat.replace(',','.'))
        
    
        ice_lon = hei['Longitude, E'].values[0]
        ice_lon = ice_lon.replace(',','.')
        ice_lon = float(ice_lon.replace('−','-'))
        if ice_lon < 0:
            ice_lon = ice_lon+360
        else:
            print(ice_lon)
        
        icelat.append(ice_lat)
        icelon.append(ice_lon)
    
    ice_year = obs['Mid_Year'].values
    ice_year = [float(item.replace(",", ".")) for item in ice_year]
    
    ice_data = obs[name]

    return ice_data[::-1], ice_year[::-1], icelat, icelon


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
        #print(point11)
        #print(point11.squeeze()+point10.squeeze()+point1_1.squeeze()+point_11.squeeze()+point_10.squeeze()+point_1_1.squeeze()+point01.squeeze()+point00.squeeze()+point0_1.squeeze())
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

def make_anomalies(model, var, lati, long, Xtragrid=False,precip=False):
    seq_list = []
    list1 = []
    path = '/home/kristineom/Documents/phdgreier/ice_cores/scratch/' # THIS IS WHERE THE PATH CHANGES
    wet = 'wet'+var
    dry = 'dry'+var

    
    for file in glob.glob(path+wet+'_*'+model+'_*historical*.nc'):
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
        

    for file1 in glob.glob(path+dry+'_*'+model+'_*historical*.nc'):
        print(file1)
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
    

    if Xtragrid == True:
        torr = find_3x3matrix(torr, lati,long)
        vaat = find_3x3matrix(vaat, lati,long)
        
        #I want mg/m2/yr so i need to multiply with 1000000/3.1688E-8
        torr = torr*(1E6/3.17098E-8)
        vaat = vaat*(1E6/3.17098E-8)
    else:
        
        torr = torr.sel(lat=lati,lon=long,method='nearest') #  "kg m-2 s-1" 
        vaat = vaat.sel(lat=lati,lon=long,method='nearest') #  "kg m-2 s-1" 

        
        #I want mg/m2/yr so i need to multiply with 1000000/3.1688E-8
        torr = torr.groupby('time.year').mean()*(1E6/3.17098E-8)
        vaat = vaat.groupby('time.year').mean()*(1E6/3.17098E-8)
        
    if precip==True: #This is we want to remove the precip dependency and make the ice core data into ng/g
        list2 =[]
        for file2 in glob.glob(path+'pr_*'+model+'_*historical*.nc'):
            print(file2)
            prec = xr.open_dataset(file2)['pr']
            list2.append(prec)
        
        if len(list2) > 1:
            print('More than one file per model and exp - must concatenate')
            concatted = xr.concat(list2,dim='time')
            prec = concatted.sortby('time')
        elif len(list2)==0:
            print('NO MATCHES FOR THIS MODEL: ',model)
            sys.exit()
        else:
            prec = list2[0]
            
        for areafile in glob.glob(path+'areacella_*'+model+'_*.nc'):
            print(areafile)
            areafile = xr.open_dataset(areafile)['areacella']
            
        if Xtragrid==True:
            area = find_3x3matrix(areafile,lati,long,True)
            prec = find_3x3matrix(prec,lati,long)
            prec = prec*area.values*(365*24*60*60) #kg
        else:
            area = areafile.sel(lat=lati,lon=long,method='nearest')
            prec = prec.sel(lat=lati,lon=long,method='nearest')
            prec = prec.groupby('time.year').mean()*area.values*(365*24*60*60) # kg
        
                
        torr = (torr/(1E6/3.17098E-8))*(365*24*60*60)                      # kg
        vaat = (vaat/(1E6/3.17098E-8))*(365*24*60*60)                      # kg
        
        depo = np.absolute(torr)+ np.absolute(vaat)
        
        dep= (depo/prec)*(1000000000000/1000)                              # change from kg/kg to ng/g
        return dep        
    
    else:
        depo = np.absolute(torr)+ np.absolute(vaat)
        return depo

def MA(values, window):
    sma = xr.DataArray(values,dims='time').rolling(time=window,min_periods=1,center=True).mean()
    return sma

def compare(location):
    models =  ['NorESM2-LM']#,'MPI-ESM-1-2-HAM','CNRM-ESM2-1','CESM2','GFDL-ESM4','INM-CM4-8', 'INM-CM5-0',
          #'CanESM5','GISS-E2-1-H','GISS-E2-1-G','CESM2-WACCM']
    
    #models = ['GISS-E2-1-G','CESM2-WACCM']
    
    if "green" in location:
        data, year, lat, lon = find_icecore_greenland(location)
        data = data/1E3 #from ug to mg

        fig, (ax1,ax3) = plt.subplots(1,2,figsize=(12,4))
        
        #color = 'tab:black'
        ax1.set_xlabel('Year')
        ax1.set_ylabel('mg m^-2 yr^-1', color='black')
        ax1.plot(year,MA(data,5), color='black',label='Ice core',linewidth=2)
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(bottom=0)
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        color = 'tab:blue'
        ax2.set_ylabel('mg m^-2 yr^-1', color=color)  # we already handled the x-label with ax1
        for i in range(len(models)):
            modeldep = []
            for j in range(len(lat)):
                dep = make_anomalies(models[i], 'so4', lat[j], lon[j],True)   #THIS IS WHERE YOU SWITCH BETWEEN 3x3 (True) AND 1x1 (False)
                modeldep.append(dep.values)
                depyear = dep.year
            dep = np.mean(modeldep,axis=0)
            if 'NorESM' in models[i]:
                ax2.plot(depyear,MA(dep,5),label=models[i],linewidth=1.8)
            elif 'EC-Earth' in models[i]:
                ax2.plot(depyear,MA(dep,5),label=models[i],linewidth=1.8)
            else:
                ax2.plot(depyear,MA(dep,5),label=models[i],linewidth=0.6)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylim(bottom=0)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax3.legend(lines + lines2, labels + labels2, loc=0)
    
        plt.title(location)
    
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.savefig('/home/kristineom/Documents/phdgreier/ice_cores/images/'+location+'_icecore_3x3_noresm.eps')
        plt.show()

        
    else:
        data, year, lat, lon = find_icecore(location)
        data = data/1E3 #from ug to mg

        fig, (ax1,ax3) = plt.subplots(1,2,figsize=(12,4))
        
        #color = 'tab:black'
        ax1.set_xlabel('Year')
        ax1.set_ylabel('mg m^-2 yr^-1', color='black')
        ax1.plot(year,MA(data,5), color='black',label='Ice core',linewidth=2)
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.set_ylim(bottom=0)
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        color = 'tab:blue'
        #ax2.set_ylabel('mg m^-2 yr^-1', color=color)  # we already handled the x-label with ax1
        ax2.set_ylabel('ng/g', color=color)
        for i in range(len(models)):
            dep = make_anomalies(models[i], 'so4', lat, lon,Xtragrid=True,precip=True)        #THIS IS WHERE YOU SWITCH BETWEEN 3x3 (True) AND 1x1 (False)
            if 'NorESM' in models[i]:
                ax2.plot(dep.year,MA(dep.values,5),label=models[i],linewidth=1.8)
            elif 'EC-Earth' in models[i]:
                ax2.plot(dep.year,MA(dep.values,5),label=models[i],linewidth=1.8)
            elif 'MPI-ESM' in models[i]:
                ax2.plot(dep.year,MA(dep.values,5),label=models[i],linewidth=1.8)
            else:
                ax2.plot(dep.year,MA(dep.values,5),label=models[i],linewidth=0.6)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylim(bottom=0)
    
    
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        
        ax3.legend(lines + lines2, labels + labels2, loc=0)
        
        plt.title(location)
        
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.savefig('/home/kristineom/Documents/phdgreier/ice_cores/images/'+location+'_icecore_3x3_test.eps')
        plt.show()


    
names = ['ACT2', 'ACT3', 'D4', 'D5', 'NGT_B19', 'Tunu13', 'McBales', 'Summit_2010', 'NEEM_2011_S1', 'NEEMS3', 
 'Humboldt', 'Akademii Nauk', 'Mt Logan', 'French Alps Ave', 'Col_du_Dome_CD10', 'Col_du_Dome_CDK', 
 'Colle Gnifetti', 'Mt. Elbrus', 'Mt. Belukha']#,'Sgreen Ave','Ngreen Ave']

plots = ['Akademii Nauk', 'Mt Logan', 'French Alps Ave','Colle Gnifetti', 'Mt. Elbrus', 'Mt. Belukha','Sgreen Ave','Ngreen Ave']
#plots = ['Sgreen Ave']
compare(names[13])

#data, year, lat, lon = find_icecore_greenland("Sgreen Ave")
#for i in range(len(plots)):
#    compare(plots[i])


