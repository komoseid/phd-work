#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:00:03 2021
Function to find right variables for ice core study for a selection of models in CMIP6
@author: Kine Onsum Moseid
"""
# on betzy: /trd-project1/NS9252K/ESGF/CMIP6/CMIP

def pathfinder(model,var):
    if 'GISS-E2-1-' in model:
        # Both models have pr and bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/historical/r1i1p3f1/AERmon/wet'+var+'/gn/v20*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/historical/r1i1p3f1/AERmon/dry'+var+'/gn/v20*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/AERmon/wet'+var+'/gn/v20*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/AERmon/dry'+var+'/gn/v20*/*'
    elif 'EC-Earth3-AerChem' in model:
        # This model has bc as below
        # This model has pr in similar path but grid is "gr" 
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        
    elif 'MPI-ESM-1-2-HAM' in model:
        # Has pr in historical r1i1p1f1 and picontrol as below
        # Has bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r3i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r3i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*' 
    elif 'CESM2' in model:
        # both models have pr and bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*.nc'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*.nc'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*.nc'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*.nc'
    elif 'CanESM5' in model:
        # Has pr and bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
    elif 'INM-CM' in model:
        # Both models have pr and bc as below 
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
    elif 'GFDL-ESM4' in model:
        # Has pr and bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
    elif 'CNRM-ESM2-1' in model:
        # Has pr and bc as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/AERmon/wet'+var+'/gr/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/AERmon/dry'+var+'/gr/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/AERmon/wet'+var+'/gr/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/AERmon/dry'+var+'/gr/v*/*'
    elif 'NorESM2' in model:
        # Both has pr as below
        # MM is missing both so4 and bc in piControl
        histwet = 'CMIP6/CMIP/NCC/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gn/latest/*'
        histdry = 'CMIP6/CMIP/NCC/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gn/latest/*'
        ctrlwet = 'CMIP6/CMIP/NCC/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/latest/*'
        ctrldry = 'CMIP6/CMIP/NCC/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/latest/*'
    
    return histwet, histdry, ctrlwet, ctrldry


def pr_pathfinder(model):
    if 'GISS-E2-1-' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/historical/r1i1p3f1/Amon/pr/gn/v20*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/Amon/pr/gn/v20*/*'
        area   = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/fx/areacella/gn/latest/areacella_fx_'+model+'_piControl_r1i1p3f1_gn.nc'
    elif 'EC-Earth3-AerChem' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/Amon/pr/gr/v*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/piControl/r1i1p1f1/Amon/pr/gr/v*/*'
        area   = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/fx/areacella/gr/latest/areacella_fx_EC-Earth3-AerChem_historical_r1i1p1f1_gr.nc'
    elif 'MPI-ESM-1-2-HAM' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r1i1p1f1/Amon/pr/gn/v*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/piControl/r1i1p1f1/Amon/pr/gn/v*/*' 
        area   =  'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_MPI-ESM-1-2-HAM_historical_r1i1p1f1_gn.nc'
    elif 'CESM2' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/Amon/pr/gn/v*/*.nc'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/piControl/r1i1p1f1/Amon/pr/gn/v*/*.nc'
        area   = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_'+model+'_historical_r1i1p1f1_gn.nc'
    elif 'CanESM5' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/Amon/pr/gn/latest/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p1f1/Amon/pr/gn/latest/*'
        area = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_CanESM5_historical_r1i1p1f1_gn.nc'
    elif 'INM-CM' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/historical/r1i1p1f1/Amon/pr/gr1/v*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/Amon/pr/gr1/v*/*'
        area   = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/fx/areacella/gr1/latest/areacella_fx_'+model+'_historical_r1i1p1f1_gr1.nc'
    elif 'GFDL-ESM4' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/Amon/pr/gr1/v*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/Amon/pr/gr1/v*/*'
        area   =  'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/fx/areacella/gr1/latest/areacella_fx_GFDL-ESM4_historical_r1i1p1f1_gr1.nc'
    elif 'CNRM-ESM2-1' in model:
        histpr = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/Amon/pr/gr/v*/*'
        ctrlpr = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/Amon/pr/gr/v*/*'
        area   = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/historical/r1i1p1f2/fx/areacella/gr/latest/areacella_fx_CNRM-CM6-1_historical_r1i1p1f2_gr.nc'
    elif 'NorESM2' in model:
        histpr = 'CMIP6/CMIP/NCC/'+model+'/historical/r1i1p1f1/Amon/pr/gn/latest/*'
        ctrlpr = 'CMIP6/CMIP/NCC/'+model+'/piControl/r1i1p1f1/Amon/pr/gn/latest/*'
        area   = 'CMIP6/CMIP/NCC/NorESM2-LM/historical/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_NorESM2-LM_historical_r1i1p1f1_gn.nc'
    return histpr, ctrlpr, area

"""
        histwet = '/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = '/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = '/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = '/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        
"""        
