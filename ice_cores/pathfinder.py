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
        # Both GISS models has pr available with same path as below
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/historical/r1i1p3f1/AERmon/wet'+var+'/gn/v20*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/historical/r1i1p3f1/AERmon/dry'+var+'/gn/v20*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/AERmon/wet'+var+'/gn/v20*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NASA-GISS/'+model+'/piControl/r1i1p3f1/AERmon/dry'+var+'/gn/v20*/*'
    elif 'EC-Earth3-AerChem' in model:
        # This model does not have bc nor pr
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/EC-Earth-Consortium/EC-Earth3-AerChem/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        
    elif 'MPI-ESM-1-2-HAM' in model:
        # 
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r3i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/historical/r3i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/HAMMOZ-Consortium/MPI-ESM-1-2-HAM/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*' 
    elif 'CESM2' in model:
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*.nc'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*.nc'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*.nc'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NCAR/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*.nc'
    elif 'CanESM5' in model:
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
    elif 'INM-CM' in model:
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/INM/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
    elif 'GFDL-ESM4' in model:
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/historical/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/AERmon/wet'+var+'/gr1/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/AERmon/dry'+var+'/gr1/v*/*'
    elif 'CNRM-ESM2-1' in model:
        histwet = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/AERmon/wet'+var+'/gr/v*/*'
        histdry = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/AERmon/dry'+var+'/gr/v*/*'
        ctrlwet = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/AERmon/wet'+var+'/gr/v*/*'
        ctrldry = 'NS9252K/ESGF/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/AERmon/dry'+var+'/gr/v*/*'
    elif 'NorESM2' in model:
        histwet = 'CMIP6/CMIP/NCC/'+model+'/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = 'CMIP6/CMIP/NCC/'+model+'/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = 'CMIP6/CMIP/NCC/'+model+'/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = 'CMIP6/CMIP/NCC/'+model+'/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        
    return histwet, histdry, ctrlwet, ctrldry

"""
        histwet = '/historical/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        histdry = '/historical/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        ctrlwet = '/piControl/r1i1p1f1/AERmon/wet'+var+'/gn/v*/*'
        ctrldry = '/piControl/r1i1p1f1/AERmon/dry'+var+'/gn/v*/*'
        
"""        
