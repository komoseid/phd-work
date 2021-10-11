

models = ['MRI-ESM2-0','GISS-E2-1-G','CNRM-ESM2-1','NorESM2-LM','GFDL-ESM4','MIROC6']
lifetime_aer = [5.9,3.8,3.9,5.7,7.9,5.7]
lifetime_bc = [7.3,3.8,3.9,6.3,0,5.7]
lifetime_so2 = [5.9,4.1,4.3,5.3,0,4.8]

atmabs_aer = [2.7,0.94,0.75,1.58,2.42,0.98]
atmabs_bc = [2.96,0.72,0.69,0.86,0,-0.07]
atmabs_so2 = [0.57,0.08,0.14,0.64,0,-0.27]

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure()
plt.plot(lifetime_aer,atmabs_aer,'o',ms=10,color='red',label='aer')
plt.plot(lifetime_bc,atmabs_bc,'o',color='blue',label='bc')
plt.plot(lifetime_so2,atmabs_so2,'o',color='green',label='so2')
plt.ylabel('Atm Abs')
plt.xlabel('BC Lifetime')
sns.despine()
plt.legend()
plt.show()