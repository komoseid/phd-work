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

def globalmean(array):
    latitude = array['lat']
    latitude_radians = latitude * np.pi / 180
    weight = np.cos(latitude_radians)
    
    array = array.mean(dim='lon')
    array = (array*weight)/np.sum(weight)
    array = array.sum(dim='lat')     
    #array = array.groupby('time.year').mean() #commented out as this func is too slow and does not weight by month, which is important when calc radiative properties
    
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


def get_globmeanyrly(var, model, experi):
    # This function looks trough a specific folder to find the piClim-experiment and corresponding piClim-control files 
    # for the variable and model of your choice.
    # It then calculates a global mean and returns yearly values as an array for both control and experiment. 
    seq_list = []
    path = '/trd-project1/NS9252K/'
    
    # Some models differ in their realizations between experiments and therefore need to be handled carefully
    if 'GISS' in model:
        if 'VOC' in experi:
            realize = 'r1i1p3f1'
        elif 'DMS' in experi:
            realize = 'r1i1p3f1'
        elif '2xss' in experi:
            realize = 'r1i1p3f1'
        elif 'dust' in experi:
            realize = 'r1i1p3f1'
        elif 'BC' in experi:
            realize = 'r1i1p3f1'
        else:
            realize = 'r1i1p1f1'
    elif 'IPSL' in model:
        if '4xCO2' in experi:
            realize = 'r2i1*'
        elif 'ghg' in experi:
            realize = 'r2i1*'
        else:
            realize = 'r1i1*'
    else:
        realize = 'r1i*'


    for file in glob.glob(path+'ESGF/CMIP6/*/*/'+model+'/piClim-control/'+realize+'/Amon/'+var+'/*/v*/*'):
        file = xr.open_dataset(file)[var]
        seq_list.append(file)
    if len(seq_list) > 1:
        #print('More than one file per model and exp - must concatenate')
        concatted = xr.concat(seq_list,dim='time')
        var_ctrl = concatted.sortby('time')
    elif len(seq_list)==0:
        print('NO MATCHES FOR ',var,' AND ',model,' FOR EXP: piClim-control')
        sys.exit()
    else:
        var_ctrl = seq_list[0]

    
    var_ctrl = globalmean(var_ctrl)

    seq_list1 = []
    for file1 in glob.glob(path+'ESGF/CMIP6/*/*/'+model+'/piClim-'+experi+'/'+realize+'/Amon/'+var+'/*/v*/*'):
        #print(file1)
        file1 = xr.open_dataset(file1)[var]
        seq_list1.append(file1)
    if len(seq_list1) > 1:
        #print('More than one file per model and exp - must concatenate')
        concatted1 = xr.concat(seq_list1,dim='time')
        var_exp = concatted1.sortby('time')
    elif len(seq_list1)==0:
        print('NO MATCHES FOR ',var,' AND ',model,' FOR EXP: ',experi)
        sys.exit()
    else:
        var_exp = seq_list1[0]

    var_exp = globalmean(var_exp)
    
    # Sometimes the ctrl and exp are run for different lengths, this confuses the calc of ERF
    if len(var_exp) < len(var_ctrl):
        var_ctrl = var_ctrl[0:len(var_exp)]
    elif len(var_exp) > len(var_ctrl):
        var_exp = var_exp[0:len(var_ctrl)]
    
    return var_ctrl, var_exp
    

def calc_ERFetc(model, experiment):
    
    rsut_ctrl, rsut_exp = get_globmeanyrly('rsut',model,experiment)
    rsdt_ctrl, rsdt_exp = get_globmeanyrly('rsdt',model,experiment)
    rsus_ctrl, rsus_exp = get_globmeanyrly('rsus',model,experiment)
    rsds_ctrl, rsds_exp = get_globmeanyrly('rsds',model,experiment)
    rsuscs_ctrl, rsuscs_exp = get_globmeanyrly('rsuscs',model,experiment)
    rsdscs_ctrl, rsdscs_exp = get_globmeanyrly('rsdscs',model,experiment)
    rsutcs_ctrl, rsutcs_exp = get_globmeanyrly('rsutcs',model,experiment)

    ERF = np.mean((np.absolute(rsdt_exp) - np.absolute(rsut_exp)) - (np.absolute(rsdt_ctrl) - np.absolute(rsut_ctrl)))
    ERF_surf = np.mean((np.absolute(rsds_exp) - np.absolute(rsus_exp)) - (np.absolute(rsds_ctrl) - np.absolute(rsus_ctrl)))
    atm_abs = ERF - ERF_surf
    
    ERFcs = np.mean((np.absolute(rsdt_exp) - np.absolute(rsutcs_exp)) - (np.absolute(rsdt_ctrl) - np.absolute(rsutcs_ctrl)))
    ERF_surfcs = np.mean((np.absolute(rsdscs_exp) - np.absolute(rsuscs_exp)) - (np.absolute(rsdscs_ctrl) - np.absolute(rsuscs_ctrl)))
    atm_abs_cs = ERFcs - ERF_surfcs
    
    return ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abs_cs



def calc_ERFetc_LW(model, experiment):
    
    rsut_ctrl, rsut_exp = get_globmeanyrly('rsut',model,experiment)
    rsdt_ctrl, rsdt_exp = get_globmeanyrly('rsdt',model,experiment)
    rsus_ctrl, rsus_exp = get_globmeanyrly('rsus',model,experiment)
    rsds_ctrl, rsds_exp = get_globmeanyrly('rsds',model,experiment)

    rlut_ctrl, rlut_exp = get_globmeanyrly('rlut',model,experiment)
    rlus_ctrl, rlus_exp = get_globmeanyrly('rlus',model,experiment)
    rlds_ctrl, rlds_exp = get_globmeanyrly('rlds',model,experiment)   
    
    rsuscs_ctrl, rsuscs_exp = get_globmeanyrly('rsuscs',model,experiment)
    rsdscs_ctrl, rsdscs_exp = get_globmeanyrly('rsdscs',model,experiment)
    rsutcs_ctrl, rsutcs_exp = get_globmeanyrly('rsutcs',model,experiment)

    #rluscs_ctrl, rluscs_exp = get_globmeanyrly('rluscs',model,experiment)
    rldscs_ctrl, rldscs_exp = get_globmeanyrly('rldscs',model,experiment)
    rlutcs_ctrl, rlutcs_exp = get_globmeanyrly('rlutcs',model,experiment)

    

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
    rsntcs_exp = (np.absolute(rsdt_exp) - np.absolute(rsutcs_exp))
    rsntcs_ctrl = (np.absolute(rsdt_ctrl) - np.absolute(rsutcs_ctrl))
    rlntcs_exp = ( np.absolute(rlutcs_exp))
    rlntcs_ctrl = ( np.absolute(rlutcs_ctrl))
    # surface
    rsnscs_exp = (np.absolute(rsds_exp) - np.absolute(rsuscs_exp))
    rsnscs_ctrl = (np.absolute(rsds_ctrl) - np.absolute(rsuscs_ctrl))
    rlnscs_exp = ( np.absolute(rldscs_exp) - np.absolute(rlus_exp))
    rlnscs_ctrl = (np.absolute(rldscs_ctrl) - np.absolute(rlus_ctrl))
    
    
    ERFcs = np.mean( (rsntcs_exp - rsntcs_ctrl) - (rlntcs_exp - rlntcs_ctrl)) 
    ERF_surfcs = np.mean((rsnscs_exp - rsnscs_ctrl) - (rlnscs_exp - rlnscs_ctrl))
    atm_abs_cs = ERFcs - ERF_surfcs
    
    #return ERF.values, ERF_surf.values, atm_abs.values, ERFcs.values, ERF_surfcs.values, atm_abs_cs.values
    return ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abs_cs

def Modellist(exp):
    # this function will return a list of models that fulfill the conditions of 
    # having rsuscs in both piclim-control and the experiment in Q.
    # I chose rsuscs as this is the variable often creating problems as 
    # it is missing. This list of models may change as Jan downloads data.
    #-----------------------------------
    matchlist = []
    pathdir = '/trd-project1/NS9252K/'
    if 'VOC' in exp:
        var = 'rsut'
    else:
        var = 'rsuscs'


    for file in glob.glob(pathdir+'ESGF/CMIP6/*/*/*/piClim-'+exp+'/r*/Amon/rsuscs/*/v*/*'):
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
    for file1 in glob.glob(pathdir+'ESGF/CMIP6/*/*/*/piClim-control/r*/Amon/rsuscs/*/v*/*'):
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
    print(combo)
    return combo

def print_tableinfo_LW(explist):
    outfile = open("/cluster/home/krisomos/rsds/ERF_LW.txt","w")
    #print(' &  &   ERF &  ERF_surf &AtmAbs& ERF CS& ERF_surf clear sky & AtmAbs CS \n')
    outfile.write('  &  &   ERF &  ERF_surf & AtmAbs & ERF CS & ERF_surf clear sky & AtmAbs CS \n')
    for i in range(len(explist)):
        outfile.write(' {0} & & & & & & & \n'.format(explist[i]))
        matchlist = Modellist(explist[i])
        print(repr('\textbf{'),explist[i],'}')
        for j in range(len(matchlist)):
            if 'NorESM' in matchlist[j]:
                #print('nei')
                ok = 'hei'
            else:
                ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abscs = calc_ERFetc_LW(matchlist[j], explist[i])
                print('&',matchlist[j],f'  & {ERF:.2f}   &   {ERF_surf:.2f}   &     {atm_abs:.2f}   &      {ERFcs:.2f}&      {ERF_surfcs:.2f}     & {atm_abscs:.2f}  \\')
                outfile.write('& {0} & {1:.2f} & {2:.2f} & {3:.2f} & {4:.2f} & {5:.2f} & {6:.2f} \\\ \n'.format(matchlist[j],ERF,ERF_surf,atm_abs, ERFcs, ERF_surfcs, atm_abscs))
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
                ERF, ERF_surf, atm_abs, ERFcs, ERF_surfcs, atm_abscs = calc_ERFetc(matchlist[j], explist[i])
                outfile.write('& {0} & {1:.2f} & {2:.2f} & {3:.2f} & {4:.2f} & {5:.2f} & {6:.2f} \\\ \n'.format(matchlist[j],ERF,ERF_surf,atm_abs, ERFcs, ERF_surfcs, atm_abscs))
                print('&',matchlist[j],f'  & {ERF:.2f}   &   {ERF_surf:.2f}   &     {atm_abs:.2f}   &      {ERFcs:.2f}&      {ERF_surfcs:.2f}     & {atm_abscs:.2f}  \\')
    outfile.close()


explist = ['2xVOC','2xDMS','2xss','2xdust','ghg','BC','aer','OC','SO2','NTCF']#'4xCO2'
#explist=['aer']
#ERF_testing( 'MRI-ESM2-0', explist[0])


print_tableinfo_LW(explist)


