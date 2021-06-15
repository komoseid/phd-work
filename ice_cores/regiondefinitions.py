#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:06:23 2019
Dirks script for defining regions
@author: kristineom
"""

def getregionlist () :
    '''
    MODIFICATION

    '''
    regionlist=['','glob','NH','SH','LAND','SEA','NHLAND','SHLAND','NHSEA','SHSEA', \
              '00N30N','30N60N','60N90N','90S28S','28S28N','28N60N', \
              '00N30NLAND','30N60NLAND','60N90NLAND','90S28SLAND','28S28NLAND','28N60NLAND', \
              '00N30NSEA' ,'30N60NSEA','60N90NSEA','90S28SSEA','28S28NSEA','28N60NSEA', \
              'NAM','SAM','NAF','SAF','SA','EA','IND','AUS', \
              'NEUR','SEUR','EUR','MED','USW','USE','US','CHN','CHNW','CHNE']
    #              'EURHTAP1','EURHTAP2']
    return regionlist




    return regionlist

def getregiondefinition (region) :
    '''
    MODIFICATION
	(2014-05-23) : included 00N30N, 30N60N, 60N90N
        (2014-10-30) : included LAND, SEA
 	(2015-01-05) : included Monsoon areas
	(2017-05-02) : added EURHTAP1, EURHTAP2
    '''
    #
    if   region=='NH'      : des={'latA' : -0., 'latB' : 90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'}
    elif region=='SH'      : des={'latA' :-90., 'latB' :  0., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'}
    elif region=='tropics' : des={'latA' :-23., 'latB' : 23., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'}
    #
    elif region=='00N30N'  : des={'latA':  0., 'latB': 30., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'}
    elif region=='30N60N'  : des={'latA': 30., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    elif region=='60N90N'  : des={'latA': 60., 'latB': 90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    elif region=='28N60N'  : des={'latA': 28., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'}  
    elif region=='28S28N'  : des={'latA':-28., 'latB': 28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    elif region=='90S28S'  : des={'latA':-90., 'latB':-28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    # land
    elif region=='00N30NLAND'  : des={'latA':  0., 'latB': 30., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'}
    elif region=='30N60NLAND'  : des={'latA': 30., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'} 
    elif region=='60N90NLAND'  : des={'latA': 60., 'latB': 90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'}
    elif region=='28N60NLAND'  : des={'latA': 28., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'}  
    elif region=='28S28NLAND'  : des={'latA':-28., 'latB': 28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'}
    elif region=='90S28SLAND'  : des={'latA':-90., 'latB':-28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'} 
    # sea
    elif region=='00N30NSEA'  : des={'latA':  0., 'latB': 30., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'} 
    elif region=='30N60NSEA'  : des={'latA': 30., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'} 
    elif region=='60N90NSEA'  : des={'latA': 60., 'latB': 90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'}
    elif region=='28N60NSEA'  : des={'latA': 28., 'latB': 60., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'}  
    elif region=='28S28NSEA'  : des={'latA':-28., 'latB': 28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'} 
    elif region=='90S28SSEA'  : des={'latA':-90., 'latB':-28., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea'} 
    #
    elif region=='global'  : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    elif region=='glob'    : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    elif region==''        : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'all'} 
    #
    elif region=='LAND' : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'}
    elif region=='SEA'  : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea' }  
    #
    elif region=='NHLAND' : des={'latA':0., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'} 
    elif region=='NHSEA'  : des={'latA':0., 'latB':90., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea' }  
    #
    elif region=='SHLAND' : des={'latA':-90., 'latB':0., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'land'} 
    elif region=='SHSEA'  : des={'latA':-90., 'latB':0., 'lonA':-180., 'lonB': 180., 'czonal':'zonal', 'cmask':'sea' }  
    #
    # Monsoon regions
    elif region=='NAM' : des={'latA':  0., 'latB':20., 'lonA':-150., 'lonB':-50., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='SAM' : des={'latA':-30., 'latB': 0., 'lonA':-120., 'lonB':-30., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='NAF' : des={'latA':  0., 'latB':15., 'lonA': -30., 'lonB': 40., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='SAF' : des={'latA':-30., 'latB': 0., 'lonA':   0., 'lonB': 90., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='SA'  : des={'latA':  5., 'latB':30., 'lonA':  70., 'lonB':105., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='EA'  : des={'latA':  0., 'latB':35., 'lonA': 105., 'lonB':180., 'cmask':'land', 'czonal':'nonzonal'}   
    elif region=='AUS' : des={'latA':-20., 'latB': 0., 'lonA':  90., 'lonB':160., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='IND' : des={'latA':  0., 'latB':30., 'lonA':  70., 'lonB': 90., 'cmask':'land', 'czonal':'nonzonal'}   
    # Europe and Middeteranean
    elif region=='NEUR': des={'latA': 45., 'latB':80., 'lonA': -10., 'lonB':30. , 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='SEUR': des={'latA': 32., 'latB':45., 'lonA': -10 , 'lonB':30. , 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='EUR' : des={'latA': 32., 'latB':80., 'lonA': -10 , 'lonB':40. , 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='MED' : des={'latA': 30., 'latB':45., 'lonA': -5. , 'lonB':40. , 'cmask':'all' , 'czonal':'nonzonal'}  #all (no land mask)
    # US
    elif region=='USW': des={'latA': 30., 'latB':48., 'lonA': -130., 'lonB':-100. , 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='USE': des={'latA': 30., 'latB':48., 'lonA': -100., 'lonB': -65. , 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='US' : des={'latA': 30., 'latB':48., 'lonA': -130., 'lonB': -65. , 'cmask':'land', 'czonal':'nonzonal'} 
    # China
    elif region=='CHN'  : des={'latA':20., 'latB':45., 'lonA': 95., 'lonB':125., 'cmask':'land', 'czonal':'nonzonal'}
    elif region=='CHNW' : des={'latA':30., 'latB':45., 'lonA': 80., 'lonB':105., 'cmask':'land', 'czonal':'nonzonal'} 
    elif region=='CHNE' : des={'latA':30., 'latB':45., 'lonA':105., 'lonB':125., 'cmask':'land', 'czonal':'nonzonal'} 
    #
    # PDRMIP - Tao et al. [2017]
    elif region=='MEDBIS' : des={'latA': 30., 'latB':45., 'lonA': -10. , 'lonB':30. , 'cmask':'all' , 'czonal':'nonzonal'}
    #
    # HTAP1 (mail Jan Eiof 2017-05-02) and HTAP2
    elif region=='EURHTAP1' : des={'latA': 25., 'latB':65., 'lonA': -10. , 'lonB':50. , 'cmask':'all' , 'czonal':'nonzonal'}
    elif region=='EURHTAP2' : des={'latA':-90., 'latB':90., 'lonA':-180., 'lonB': 180., 'cmask':region, 'czonal':'nonzonal'}
    else : quit()
    # 
    return des


#SEA = (getregiondefinition("EUR"))
#print(SEA["latB"])
#print(SEA['lonB'])