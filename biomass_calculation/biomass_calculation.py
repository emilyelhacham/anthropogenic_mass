#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load dependencies 
import numpy as np
import pandas as pd
from collections import defaultdict
import os


# # Biomass estimation
# 
# Our biomass calculation estimation is divided into two time periods: 1900-1990 & 1990-2017.
# We first estimate the plant biomass, which represents ≈90% of the global biomass [(Bar-On et al., 2018](https://doi.org/10.1073/pnas.1711842115)[, 2019)](https://doi.org/10.1038/s41579-019-0162-0). 
# 
# 
# ## 1990-2017 plant biomass estimation
# 
# Our plant biomass value for 2010 is based on [(Bar-On et al.)](https://doi.org/10.1073/pnas.1711842115), which relies on [(Erb et al.)](https://doi.org/10.1038/nature25138) estimate which consists of the mean of seven different global plant biomass maps, based on inventories or remote sensing.
# 
# To estimate the total plant biomass for the years 1990-2017, we rely on two approaches:
# 1. Based on three main data sources, employing inventory measurements or remote sensing ([Pan et al.](https://doi.org/10.1126/science.1201609); [Liu et al.](https://doi.org/10.1038/nclimate2581); [FRA 2010](http://www.fao.org/3/i1757e/i1757e.pdf) followed by [FAOSTAT](http://faostat.fao.org) for later years).
# 2. Based on ensemble of 15 Dynamic Global Vegetation Models [(TRENDY)](https://sites.exeter.ac.uk/trendy).
# 
# 
# We use plant biomass estimates of five different time points (1990, 2000, 2010, 2012, 2017), chosen according to data availability (for Pan et al., we used the 2007 estimate; for Liu et al. we used the 1993 estimate as 1990). 

# In[2]:


# Upload biomass estimates from different sources, units [GtC] 
bm_est = pd.read_excel("bm_est.xlsx", index_col ="data source")


# We first normalize the estimates of the different sources in relation to our 2010 estimate, according to the plant biomass component each source includes (all plants or forests), where we divide the sources into the two approaches.

# In[3]:


# Normalize the estimates in relation to our 2010 plant biomass estimate    
approach1= defaultdict(list)
approach2 = defaultdict(list) 
PLANTS_BM = 450 
FOREST_FRAC = 0.75
for source in set(bm_est.index):
    est_dic = dict(zip(np.array(bm_est.loc[source]['year']), np.array(bm_est.loc[source]['biomass [GtC]'])))
    for year in est_dic.keys():
        if year != 2010:
            if (source == 'Liu et al.'):
                approach1[year].append(est_dic[year]/est_dic[2010] * PLANTS_BM)
            if (source == 'DGVM'):
                approach2[year].append(est_dic[year]/est_dic[2010]  * PLANTS_BM)
            if (source == 'FRA2010') or (source == 'Pan et al.') or (source == 'FAOstat'):
                approach1[year].append(((est_dic[year]*(1/FOREST_FRAC))/(est_dic[2010]*(1/FOREST_FRAC))) * PLANTS_BM)


# Next, for each time point, we take the mean of the normalized biomass estimates across the different sources, to obtain the biomass estimate for each of the time points. To generate our best estimate, we take the mean of the two approaches: 
# 1. Inventory measurements or remote sensing
# 2. Dynamic Global Vegetation Models

# In[4]:


# Calculate the best estimate for each year for each approach, which is the mean of all sources within the approach
bm_plants = {2010: PLANTS_BM}
for year in ([1990,2000,2012,2017]):
    bm_plants[year] = (np.mean(np.array([np.mean(approach1[year]),approach2[year][0]])))


# ## 1900-1990 plant biomass estimation
# 
# The 1900-1900 estimate relies on the 15 [Dynamic Global Vegetation Models ensemble](https://sites.exeter.ac.uk/trendy) annual mean, which was normalized according to our 1990 estimate, calculated above.

# In[5]:


# Upload plant biomass estimates of the Dynamic Global Vegetation Models ensemble, units [GtC]
dgvm = pd.read_excel('DGVM_mean.xlsx')


# In[6]:


# Normalize the estimates in relation to our 2010 biomass estimate 
for i in xrange(91):
    bm_plants[1900+i]= (dgvm.iloc[i,1]/dgvm.iloc[90,1]* bm_plants[1990])


# ## Overall biomass estimate
# 
# As a final step, the non-plant biomass was added to the plant biomass. 
# The non-plant estimate was derived according to [(Bar-On et al.)](https://doi.org/10.1073/pnas.1711842115), with updates for the biomass of bacteria and archaea kingdoms [(Magnabosco et al.,](https://www.nature.com/articles/s41561-018-0221-6) [Bar-On et al.)](https://doi.org/10.1038/s41579-019-0162-0).

# In[7]:


# Add non-plant biomass 
years = np.array(bm_plants.keys())
plants = np.array(bm_plants.values())
NON_PLANT_BM = 48.2
bm = plants + NON_PLANT_BM


# ## Biomass extrapolation 2018-2037
# 
# To extrapolate the future biomass change, we use the linear rate of change calculated for 2010-2017, and assume it remains constant.

# In[8]:


# Calculate rate of change 2010-2017 
trend = np.polyfit(years[-3:],bm[-3:],1)[0]

# Apply the rate to future years 
years_ext = np.linspace(2018,2037,20)
for i in xrange(len(years_ext)):
    bm = np.append(bm,bm[-1]+trend)

years = np.concatenate([years,years_ext])


# ### Conversion of carbon-weight basis to dry-weight basis 
# 
# To convert the biomass to a dry-weight basis, we multiply by the corresponding conversion factor.

# In[9]:


CFACTOR = 2.25
bm_d = CFACTOR * bm


# ### Conversion of dry-weight basis to wet-weight basis
# 
# To convert the biomass to a wet-weight basis, we multiply by the corresponding conversion factor.

# In[10]:


WFACTOR = 2.0
bm_w = WFACTOR * bm_d


# #### Saving biomass data into file

# In[11]:


file_path = os.path.abspath('')


# In[12]:


bm_tot = pd.DataFrame({'biomass (Tt)': bm_d/1000, 'year':np.int_(years)})
bm_tot.to_excel(file_path + "/../data/biomass_dry.xlsx", index=False)
bmw_tot = pd.DataFrame({'biomass (Tt)': bm_w/1000, 'year':np.int_(years)})
bmw_tot.to_excel(file_path + "/../data/biomass_wet.xlsx", index=False)

