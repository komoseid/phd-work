import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import warnings
from dask.diagnostics import ProgressBar
import icecore_ratios as icefunc
warnings.simplefilter("ignore")
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

models =  ['MPI-ESM-1-2-HAM','CESM2','CESM2-WACCM','CNRM-ESM2-1','GISS-E2-1-H','GISS-E2-1-G','NorESM2-LM',
           'MRI-ESM2-0', 'MIROC6','EC-Earth3-AerChem','GFDL-ESM4']

def makefig(models):
    fig,axs = plt.subplots(2,4,figsize=(15,5))
    #i= 0
    namelist = ['ACT2', 'ACT11D', 'D4', 'Summit2010','NGT_B19', 'Tunu2013', 'NEEM_2011_S1',  'Humboldt']
    for i,ax in enumerate(fig.axes):
        for model in models:
            ratios,years = icefunc.make_model_ratios(model,namelist[i],5)
            ax.plot(years,ratios,color=colors[model])

        iceratio, iceyears = icefunc.make_icecore_ratios(namelist[i],5)
        ax.plot(iceyears,iceratio,linewidth=3,color='black')
        ax.set_title(namelist[i])
        ax.set_ylim([0,0.42])
        ax.set_xlim([1850,2014])
        #i +=1

    plt.savefig('/home/kristineom/Documents/phdgreier/lifetimes/images/testing.png')
    plt.show()
    #print(ratios,years)

makefig(models)