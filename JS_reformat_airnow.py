#!/usr/bin/env python
# coding: utf-8

# ## MONET-Analysis Airnow prep notebook
# 
# ### How to use
# 
# - start notebook and 
# - in cell 2 set the start date and end date
# - in cell 2 set the filename output (something like AIRNOW_STARTDATE_ENDDATE.nc with STARTDATE and ENDDATE in YYYYMMDD format)

# In[ ]:

import sys
import monetio as mio
import pandas as pd
import xarray as xr
from melodies_monet.util import write_util


# In[ ]:
filename = 'full_AIRNOW_20230702_20230729.nc'
#dates = pd.date_range(start='2020-09-06',end='2020-09-11',freq='H')
#filename = 'AIRNOW_20190901_20190902.nc'
dates = pd.date_range(start='2023-07-02',end='2023-07-31',freq='H')

# helper function for local time.  Could be important for EPA statistics
def get_local_time(ds):
    from numpy import zeros
    if 'utcoffset' in ds.data_vars:
        tim = t.time.copy()
        o = tim.expand_dims({'x':t.x.values}).transpose('time','x')
        on = xr.Dataset({'time_local':o,'utcoffset':t.utcoffset})
        y = on.to_dataframe()
        y['time_local'] = y.time_local + pd.to_timedelta(y.utcoffset, unit='H')
        time_local = y[['time_local']].to_xarray()
        ds = xr.merge([ds,time_local])
    return ds


# In[ ]:


df = mio.airnow.add_data(dates,wide_fmt=False,n_procs=12)


# In[ ]:


df = df.dropna(subset=['latitude','longitude']) # drop all values without an assigned latitude and longitude 
dfp = df.rename({'siteid':'x'},axis=1).pivot_table(values='obs',index=['time','x'], columns=['variable']) # convert to wide format
dfx = dfp.to_xarray() # convert to xarray 
# df.head()


# In[ ]:


# When converting to wide format we have to remerge the site data back into the file.  
dfpsite = df.rename({'siteid':'x'},axis=1).drop_duplicates(subset=['x']) # droping duplicates and renaming 
# convert sites to xarray 
test = dfpsite.drop(['time','time_local','variable','obs'],axis=1).set_index('x').dropna(subset=['latitude','longitude']).to_xarray()
# merge sites back into the data 
t = xr.merge([dfx,test])
# get local time
tt = get_local_time(t)


# In[ ]:


# add siteid back as a variable and create x as an array of integers 
tt['siteid'] = (('x'),tt.x.values)
tt['x'] = range(len(tt.x))
# expand dimensions so that it is (time,y,x)
t = tt.expand_dims('y').set_coords(['siteid','latitude','longitude']).transpose('time','y','x')
t


# In[ ]:


#wite out to filename set in cell 2
write_util.write_ncf(t,filename)


# In[ ]:





# In[ ]:




