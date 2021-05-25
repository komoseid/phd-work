# Example script

The python script in this folder will read the csv-file containing concetration of black carbon as measured at the Upper Freeman Glacier.
It will also read a selection of model files and calculate the yearly concentration of BC from the model CanESM5. 

## Python libraries needed

```
import pandas as pd
import numpy as np
import sys,os,glob
import xarray as xr
```

## Usage
If cloning this repository you need to change the path from
```python
    path = '/cluster/home/krisomos/example/'  
```
in line 61 of the script "examplescript.py" to the path where you store the *.nc and *.csv files from this repository. 

"examplescript.py" contains functions which is called in the end of the script
```python
ice_conc, iceyear, icelat, icelon = icecore_info()
model_conc = make_concentration(icelat,icelon)
print(ice_conc,model_conc)
```
The concentrations are currently just printed, but plotting them together is encouraged for comparing model concentration of black carbon to what is measured in an ice core

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
