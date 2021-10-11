#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:27:51 2021
sshfs krisomos@betzy.sigma2.no:/trd-project1/ betzy/
sshfs krisomos@login.nird.sigma2.no:/projects/NS9034K/ betzy_output/
sshfs krisomos@login.nird.sigma2.no:/projects/NS9560K/ NS9560K/

this script makes the lifetime vs lat per decade fig
@author: kristineom
"""
import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import cartopy.crs as ccrs
from dask.diagnostics import ProgressBar
import geonum.atmosphere as atm    # used to calculate atmospheric quanteties
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'
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
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def avgyear(lst,n):
    tenTS = list(chunks(lst,n))
    #print(tenTS)
    for chunk in range(len(tenTS)):
        if len(tenTS[chunk]) < n:
            tenTS.pop(chunk)
    datalist = []
    datalist = np.nanmean(tenTS,axis=1)
    #print(np.shape(tenTS))
    #for i in range(len(tenTS)):
        
    #    datalist.append(np.nanmean(tenTS[i],axis=1))
    return datalist

def plot_cmip6_lifetime(models,variable):
    from pathfinder import pathfinder, pr_pathfinder
    import seaborn as sns
    
    fig, axs = plt.subplots(3,4,figsize=(12,9))
    axs = axs.flatten()
    #ax1.set_xlabel('Latitude')
    #ax1.set_ylabel('lifetime', color='black')
    i = 0
    letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    for model in models:
        
        loadpath = '/home/kristineom/Documents/phdgreier/ice_cores/data/burden'+variable+'_'+model+'.nc'
        deppath = '/home/kristineom/Documents/phdgreier/ice_cores/data/totaldep'+variable+'_'+model+'.nc'

        
        load = xr.open_dataset(loadpath)['__xarray_dataarray_variable__']
        depo = xr.open_dataset(deppath)['__xarray_dataarray_variable__']
        #ratdep = xr.open_dataset(ratiodeppath)['__xarray_dataarray_variable__']
        #ratdep = ratdep.mean(dim='lon') # no 
        depo = depo.mean(dim='lon')
        load = load.sum(dim='lev')  #kg / m2
        load = load.mean(dim='lon')  # kg/m2
        lati = load.lat
        
        newload = avgyear(load,10)
        depo =  avgyear(depo,10)


        ratio = newload/depo  /(60*60*24) # days
        #ratio = ratdep
        col, row = ratio.shape
        
        #CREATE COLORMAP
        n_lines = col
        n_year = np.linspace(1850,2010,n_lines+1)
        #print(int(n_year))
        c = np.arange(1, n_lines + 1)
        #print([int(i) for i in n_year])
        norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
        cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.plasma)
        cmap.set_array([])
        

        for j in range(col):
#            if '195' in str(int(n_year[i])):
#                ax1.plot(lati, ratio[i],c='red')#,color=colors[model],label=model)
#            elif '196' in str(int(n_year[i])):
#                ax1.plot(lati, ratio[i],c='red')#,color=colors[model],label=model) 
#            elif '197' in str(int(n_year[i])):
#                ax1.plot(lati, ratio[i],c='red')#,color=colors[model],label=model)                
#            else:
            axs[i].plot(lati, ratio[j],c=cmap.to_rgba(j + 1))#,color=colors[model],label=model
        axs[i].text(0.05,0.9, model, fontsize=10,transform=axs[i].transAxes)
        #axs[i].set_title(model)
        axs[i].set_xlim(0,75)
        axs[i].set_ylim(0,18)
        sns.despine()
        axs[i].grid()
        i +=1
    leg = []
    for j in range(col):
        leg.append(mpl.patches.Patch(color=cmap.to_rgba(j+1),label=str(int(n_year[j]))))
    axs[0].set_ylabel('Days')
    axs[4].set_ylabel('Days')
    axs[8].set_ylabel('Days')
    axs[8].set_xlabel('Latitude')
    axs[9].set_xlabel('Latitude')
    axs[10].set_xlabel('Latitude')
    axs[11].legend(handles=leg,ncol=2)
    axs[11].spines['top'].set_visible(False)
    axs[11].spines['right'].set_visible(False)
    axs[11].spines['bottom'].set_visible(False)
    axs[11].spines['left'].set_visible(False)
    axs[11].get_xaxis().set_ticks([])
    axs[11].get_yaxis().set_ticks([])    
    #cbar = fig.colorbar(cmap, ticks=c)
    #cbar.axs[12].set_yticklabels([str(int(k)) for k in n_year])
    #plt.legend()
    plt.savefig('/home/kristineom/Documents/phdgreier/lifetimes/images/lifetime_per_lat.png')
    plt.show()

models =  ['MPI-ESM-1-2-HAM','CESM2','CESM2-WACCM','MRI-ESM2-0','GISS-E2-1-H','GISS-E2-1-G','NorESM2-LM', 'MIROC6',
           'EC-Earth3-AerChem','GFDL-ESM4','CNRM-ESM2-1']

#plot_cmip6_lifetime(models,'bc')

def plot_cmip6_bcratio(models):
    from pathfinder import pathfinder, pr_pathfinder
    import seaborn as sns
    
    fig, axs = plt.subplots(3,4,figsize=(12,9))
    axs = axs.flatten()
    i = 0
    letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    for model in models:
        
        loadbcpath = '/home/kristineom/Documents/phdgreier/ice_cores/data/burdenbc_'+model+'.nc'
        depbcpath = '/home/kristineom/Documents/phdgreier/ice_cores/data/totaldepbc_'+model+'.nc'
        loadsopath = '/home/kristineom/Documents/phdgreier/ice_cores/data/burdenso4_'+model+'.nc'
        depsopath = '/home/kristineom/Documents/phdgreier/ice_cores/data/totaldepso4_'+model+'.nc'

        loadbc = xr.open_dataset(loadbcpath)['__xarray_dataarray_variable__']
        depobc = xr.open_dataset(depbcpath)['__xarray_dataarray_variable__']
        loadso = xr.open_dataset(loadsopath)['__xarray_dataarray_variable__']
        deposo = xr.open_dataset(depsopath)['__xarray_dataarray_variable__']

        depobc = depobc.mean(dim='lon')
        loadbc = loadbc.sum(dim='lev')  #kg / m2
        loadbc = loadbc.mean(dim='lon')  # kg/m2
        latibc = loadbc.lat
        newloadbc = avgyear(loadbc,10)
        depobc =  avgyear(depobc,10)

        deposo = deposo.mean(dim='lon')
        loadso = loadso.sum(dim='lev')  #kg / m2
        loadso = loadso.mean(dim='lon')  # kg/m2
        latibso = loadso.lat
        newloadso = avgyear(loadso,10)
        deposo =  avgyear(deposo,10)

        ratiobc = newloadbc/depobc  /(60*60*24) # days
        ratioso = newloadso/deposo  /(60*60*24) # days
        ratio = depobc/deposo        
        #ratio = ratdep
        col, row = ratio.shape
        
        #CREATE COLORMAP
        n_lines = col
        n_year = np.linspace(1850,2010,n_lines+1)
        #print(int(n_year))
        c = np.arange(1, n_lines + 1)
        #print([int(i) for i in n_year])
        norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
        cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.plasma)
        cmap.set_array([])
        

        for j in range(col):
            axs[i].plot(latibc, ratio[j],c=cmap.to_rgba(j + 1))#,color=colors[model],label=model
        axs[i].text(0.05,0.9, model, fontsize=10,transform=axs[i].transAxes)
        axs[i].set_xlim(0,75)
        axs[i].set_ylim(0,0.2)
        sns.despine()
        axs[i].grid()
        i +=1
    leg = []
    for j in range(col):
        leg.append(mpl.patches.Patch(color=cmap.to_rgba(j+1),label=str(int(n_year[j]))))
    axs[0].set_ylabel('ratio')
    axs[4].set_ylabel('ratio')
    axs[8].set_ylabel('ratio')
    axs[8].set_xlabel('Latitude')
    axs[9].set_xlabel('Latitude')
    axs[10].set_xlabel('Latitude')
    axs[11].legend(handles=leg,ncol=2)
    axs[11].spines['top'].set_visible(False)
    axs[11].spines['right'].set_visible(False)
    axs[11].spines['bottom'].set_visible(False)
    axs[11].spines['left'].set_visible(False)
    axs[11].get_xaxis().set_ticks([])
    axs[11].get_yaxis().set_ticks([])    
    #cbar = fig.colorbar(cmap, ticks=c)
    #cbar.axs[12].set_yticklabels([str(int(k)) for k in n_year])
    #plt.legend()
    plt.savefig('/home/kristineom/Documents/phdgreier/lifetimes/images/ratio_per_lat.png')
    plt.show()

plot_cmip6_bcratio(models)


def plot_cmip6_depratio(models,variable):
    from pathfinder import pathfinder, pr_pathfinder
    
    fig, (ax1) = plt.subplots(1,1,figsize=(9,5))
    ax1.set_xlabel('year')
    ax1.set_ylabel('Ratio wet/dry', color='black')
    
    for model in models:
        loadpath = '/home/kristineom/Documents/phdgreier/ice_cores/data/burden'+variable+'_'+model+'.nc'
        deppath = '/home/kristineom/Documents/phdgreier/ice_cores/data/totaldep'+variable+'_'+model+'.nc'
        ratiodeppath = '/home/kristineom/Documents/phdgreier/ice_cores/data/ratiodep'+variable+'_'+model+'.nc'
        
        load = xr.open_dataset(loadpath)['__xarray_dataarray_variable__']
        depo = xr.open_dataset(deppath)['__xarray_dataarray_variable__']
        ratdep = xr.open_dataset(ratiodeppath)['__xarray_dataarray_variable__']
        ratdep = ratdep.mean(dim='lon') # no unit
        ratdep = ratdep.mean('lat')
        depo = depo.mean(dim='lon')
        load = load.sum(dim='lev')  #kg / m2
        load = load.mean(dim='lon')  # kg/m2
        year = load.year
        
        ax1.plot(year, ratdep,color=colors[model],label=model)#,c=cmap.to_rgba(i + 1))#,color=colors[model],label=model)
    ax1.set_title(variable+' wet/dry ')
    ax1.set_xlim(1925,2014)
    #ax1.set_ylim(0,50)
    plt.grid()
    #plt.legend()
    plt.show()
    
#plot_cmip6_depratio(models,'so4')
    
def plot_noresm_lifetime(variable):
    list_of_exp  = ['ref','bceur','bcnam','bcasi','so2eur','so2nam','so2asi','bio']
    path = '/home/kristineom/Documents/phdgreier/ice_cores/NS9560K/krisomos/'
    
    
    for exp in list_of_exp:        
        burden = path+'burden'+variable+'_NorESM2-LM_'+exp+'.nc'    
        load = xr.open_dataset(burden)['__xarray_dataarray_variable__']
        load = load.sum(dim='lev')  #kg / m2
        load = load.mean(['lon'])
        lati = load.lat

        dep = xr.open_dataset(path+'totaldep'+variable+'_NorESM2-LM_'+exp+'.nc')['__xarray_dataarray_variable__']
        dep = dep.mean(dim='lon')
        
        load = avgyear(load,10)
        dep =  avgyear(dep,10)
        
        lifet = (load/dep) /(60*60*24)     # kg/m2 / kg/m2/s 
        col, row = lifet.shape
        
        n_lines = col
        n_year = np.linspace(1850,2009,n_lines+1)
        c = np.arange(1, n_lines + 1)
        norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
        cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues)
        cmap.set_array([])        
        
        fig, (ax1) = plt.subplots(1,1,figsize=(9,5))
        ax1.set_xlabel('Latitude')
        ax1.set_ylabel('days', color='black')
        for i in range(col):  
            ax1.plot(lati,lifet[i],c=cmap.to_rgba(i + 1))#,label = labels[exp], color = colors[exp])
        cbar = fig.colorbar(cmap, ticks=c)
        cbar.ax.set_yticklabels([str(int(i)) for i in n_year])
        ax1.set_title(exp+'  '+variable+' lifetime* ')
        ax1.set_xlim(0,80)
        ax1.set_ylim(2,16)
        plt.grid()
        #plt.legend()
        plt.show()
#plot_noresm_lifetime('bc')