# this script shall calculate ratios of bc to sulfate in ice core locations
import pandas as pd
import os,glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import sys
import warnings
from dask.diagnostics import ProgressBar
warnings.simplefilter("ignore")
os.environ['HDF5_USE_FILE_LOCKING']='FALSE'

def find_mcconnell_icecore(name, var):
    # 
    #
    # Ex: data, year, lat, lon = find_mcconnell_icecore('Ngreen', 's')
    #--------------------------------------------------------------------
    obs = pd.ExcelFile('/home/kristineom/Documents/phdgreier/ice_cores/temp/Greenland_data_for_Kine_051021.xlsx')
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
            ok = 12
            #print(ice_lon)
        
        icelat.append(ice_lat)
        icelon.append(ice_lon)

        icedata = ice[newnames[i]].values
        ice_data.append(icedata)
    
    
    ice_year = ice['Mid Year'].values
    
    ice_data = np.nanmean(ice_data,axis=0) #Note that by using nanmean we ignore the icecores with nan values, so some years have a mean based on fewer sites

    return ice_data[::-1], ice_year[::-1], icelat, icelon


def find_other_icecore(name, var):
    # Works with name = ['McCall_Glacier','Eclipse','Mt Oxford','Akademii Nauk','ColDuDome','Mt Elbrus']
    # 050821 UPDATED TO ACCOUNT FOR NEGATIVE LON VALUES
    # Ex: data, year, lat, lon = find_other_icecore('UFG', 'bc')
    #--------------------------------------------------------------------
    obs = pd.ExcelFile('/home/kristineom/Documents/phdgreier/ice_cores/temp/Greenland_data_for_Kine_051521.xlsx')
    ice = pd.read_excel(obs,name)
    icename = pd.read_excel(obs,'Core Stats')

    iceinfo = icename[icename['Core'].isin([name])]

    icelat = []
    icelon = []    
    icelat.append(iceinfo['Lat'].values[0])
    icelon.append(iceinfo['Lon'].values[0])

    if icelon[0] < 0:
        icelon[0] = icelon[0]+360
    else:
        ok = 12
        
    if 'bc' in var:
        if 'ColDuDome' in name:
            ice_data = ice['CDD_annual_BC_ng/g'].values
        elif 'Elbrus' in name:
            vals = pd.ExcelFile('/home/kristineom/Documents/phdgreier/ice_cores/temp/Elbruse rBC midseasonal and annual summary_S.Lim_2021.09.03.xlsx')
            iceval = pd.read_excel(vals,'annual')
            ice_data = iceval['Mean']
            ice_year = iceval['year']
        else:
            ice_data = ice['BC_ng/g'].values
    elif 's' in var:
        if 'ColDuDome' in name:
            ice_data = ice['CDD_annual S_ng/g'].values
        else:        
            ice_data = ice['S_ng/g'].values
    
    if 'Elbrus' in name:
        if 'bc' in var:
            ok=12
        else:
            ice_year = ice['Mid_Year'].values
    else:
        ice_year = ice['Mid_Year'].values

    return ice_data[::-1], ice_year[::-1], icelat, icelon

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def yearavg(timeseries,yearseries,numyear):
    tenyr = list(chunks(yearseries,numyear))
    tenTS = list(chunks(timeseries,numyear))
    for chunk in range(len(tenTS)):
        if len(tenTS[chunk]) < numyear:
            tenTS.pop(chunk)
            tenyr.pop(chunk)    
    #print(tenyr[-1:])
    yearlist = []
    datalist = []
    for i in range(len(tenyr)):
        yearlist.append(np.nanmean(tenyr[i]))
        datalist.append(np.nanmean(tenTS[i]))
    #print(yearlist)
    #print(datalist)
    return datalist, yearlist

def make_icecore_ratios(name,numyear):
    bcdata,year, lat, lon = find_mcconnell_icecore(name,'bc')
    so4data,year, lat, lon = find_mcconnell_icecore(name,'so4')

    newbc, newyear = yearavg(bcdata,year,numyear)
    newso4, newyear = yearavg(so4data,year,numyear)

    ratio = np.array(newbc)/np.array(newso4)

    return ratio, newyear

def open_models(model,area,var):
    #print(type(model),type(area),type(var))
    data = xr.open_dataset('/home/kristineom/Documents/phdgreier/ice_cores/betzy_temp/'+var+'_'+model+'_'+area+'_conc.nc')['Conc_Absolute']
    year = np.linspace(1850,2014,165)
    #data = data.expand_dims(time=data.year)
    if 'green' in area:
        ok=12
    else:
        data = data.rename({'year':'time'})
    #data.drop_dims('year')
    return data, year


def make_model_ratios(model,name,numyear):
    #bcdata,year, lat, lon = find_mcconnell_icecore(name,'bc')
    bcdata , year = open_models(model,name,'bc')
    so4data , year = open_models(model,name,'so4')


    newbc, newyear = yearavg(bcdata,year,numyear)
    newso4, newyear = yearavg(so4data,year,numyear)

    ratio = np.array(newbc)/np.array(newso4)

    return ratio, newyear

#data,year, lat, lon = find_mcconnell_icecore('NEEM_2011_S1','bc')
#print(data)
#newdata, newyear = yearavg(data,year,5)
#print(newdata)

