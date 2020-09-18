#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load dependencies 
import numpy as np
import pandas as pd
import os
import re
from uncertainties import ufloat
from uncertainties import unumpy
from collections import defaultdict


# # Biomass uncertainty calculation 
# 
# This notebook is complementary to the biomass calculation notebook.
# Following the biomass calculation main steps, the uncertainty is first calculated for plant biomass, followed by non-plant biomass addition and multiplication by weight conversion factors. 
# <br>In the first part, the uncertainty is derived using the Python Uncertainties Package error propagation. 
# <br>In the second part, it was estimated using Monte Carlo simulations, with each parameter randomly drawn according to its uncertainty distribution. The process is repeated 10,000 times, with the resulting distribution dictating the overall uncertainty.

# ## Uncertainty estimation for the plant biomass
# 
# The uncertainty for the plant biomass is calculated following our biomass calculation, using the Python Uncertainties Package.

# #### Uncertainty of the fraction of forests out of the total plant biomass 
# 
# As part of the biomass calculation, we use the estimate of the fraction of forest out of the total plants biomass.  To estimate the uncertainty of the fraction, we use the data on general biomes plants biomass, from [Erb et al.](https://doi.org/10.1038/nature25138).

# In[2]:


# Upload biomes biomass, from Erb et al. 
biomes_bm = pd.read_excel("general_biome_mass_Erb.xlsx")
biomes = dict(zip(list(biomes_bm['biome']), [map(int,re.findall(r'\d+', x)) for x in map(str, biomes_bm['biomass [Gt C]'])]))
biomes_bm


# To derive the corresponding uncertainty of forests out of the sum of the biomass of plants, we randomly draw the biomes plants biomass, according to the provided data, and follow the same calculation as further detailed in the biomass calculation notebook.  

# In[3]:


def get_forest_fraction(biome_dic, num):
    fforest = np.empty(0)
    for j in xrange(num):
        bm_sum = 0
        for biome in biome_dic.keys():
            if len(biome_dic[biome])>1:
                if biome == 'Forests':
                    forest = np.random.normal(np.average(biome_dic[biome]), np.std(biome_dic[biome], ddof = 1))
                    bm_sum = bm_sum +forest 
                else:
                    bm_sum = bm_sum + np.random.normal(np.average(biome_dic[biome]), np.std(biome_dic[biome], ddof = 1))
            else:
                bm_sum = bm_sum + biomes[biome][0]
        fforest = np.append(fforest,float(forest)/bm_sum)    
    return fforest             


# The process is repeated 10,000 times:

# In[4]:


num_iterations = 10000
forestf = get_forest_fraction(biomes,num_iterations)
print "forest fraction:  mean = " + str(np.mean(forestf).round(2)) + " std = "+ str(np.std(forestf).round(2))


# ### Uncertainty of plant biomass estimates (1990-2017)
# 
# We derive the uncertainty using Python Uncertainties Package error propagation.

# In[5]:


# Upload biomass estimates from different sources, units [GtC] 
bm_est = pd.read_excel("bm_est.xlsx", index_col ="data source")
dgvm = pd.read_excel("DGVM_mean.xlsx")


# In[6]:


# Normalize the estimates in relation to our 2010 plant biomass estimate    
approach1= defaultdict(list)
approach2 = defaultdict(list) 
PLANTS_BM = ufloat(450, 45)
FOREST_FRAC = ufloat(np.mean(forestf),np.std(forestf))
for source in set(bm_est.index):
    est_dic = dict(zip(np.array(bm_est.loc[source]['year']), np.array(bm_est.loc[source]['biomass [GtC]'])))
    for year in est_dic.keys():
        if year != 2010:
            if (source == 'Liu et al.'):
                approach1[year].append(est_dic[year]/est_dic[2010] * PLANTS_BM)
            if (source == 'DGVM'):
                approach2[year].append(ufloat(dgvm.iloc[year-1900,1], dgvm.iloc[year-1900,2])/est_dic[2010] * PLANTS_BM)
            if (source == 'FRA2010') or (source == 'Pan et al.') or (source == 'FAOstat'):
                approach1[year].append(((est_dic[year]*(1/FOREST_FRAC))/(est_dic[2010]*(1/FOREST_FRAC))) * PLANTS_BM )


# In[7]:


# Calculate the best estimate for each year for each approach, which is the mean of all sources within the approach
bm_plants = {2010: PLANTS_BM}
for year in ([1990,2000,2012,2017]):
    bm_plants[year] = (np.mean(np.array([np.mean(approach1[year]),approach2[year][0]])))


# ### Uncertainty of plant biomass estimates (1900-1990)
# 
# We derive the uncertainty using Python Uncertainties Package error propagation. 

# In[8]:


# Normalize the estimates in relation to our 2010 biomass estimate 
for i in xrange(90):
    bm_plants[1900+i]= (ufloat(dgvm.iloc[i,1],dgvm.iloc[i,2])/dgvm.iloc[90,1]* bm_plants[1990])


# ## Uncertainty estimation for the overall biomass
# 
# We derive the uncertainty by following our calculation steps, and randomly drawing the non-plant biomass, carbon-to-dry-weight and wet-to-dry-weight conversion factors, dynamic global vegetation models mean, as well as the 1990 plant biomass.

# In[9]:


# Add non-plant biomass and multiply by conversion factors
def get_BM_tot(num, bm_rec):
    bm_tot= defaultdict(list)
    bm_tot_w= defaultdict(list)
    for j in xrange(num):
        NON_PLANT_BM = np.random.lognormal(np.log(48.2), np.log(1.9)/1.96)
        CFACTOR = np.random.normal(2.25,0.13)
        WFACTOR = np.random.normal(2.0,0.3)
        z = np.random.normal(0,1)
        for year in bm_rec.keys():
                bm_tot[year].append(((z*bm_rec[year].s) + bm_rec[year].n + NON_PLANT_BM)* CFACTOR)
                bm_tot_w[year].append(bm_tot[year][-1]* WFACTOR)
    # averaging all runs 
    for y in bm_tot.keys():
        bm_tot[y] = ufloat((np.mean(np.array(bm_tot[y]))),(np.std(np.array(bm_tot[y]), ddof=1)))
        bm_tot_w[y] = ufloat((np.mean(np.array(bm_tot_w[y]))),(np.std(np.array(bm_tot_w[y]), ddof=1)))
    return bm_tot, bm_tot_w


# We repeat the process 10,000 times: 

# In[10]:


num_iterations = 10000
bm_dic_tot, bm_dic_tot_w = get_BM_tot(num_iterations, bm_plants)


# In[11]:


year = np.linspace(1900,1990,91)
years = np.concatenate([year,np.array([2000,2010,2012,2017])])
bm = np.empty(0)
bm_w = np.empty(0)
for year in list(years):
    bm = np.append(bm, bm_dic_tot[year])
    bm_w = np.append(bm_w, bm_dic_tot_w[year])


# #### saving biomass uncertainty data into file

# In[12]:


file_path = os.path.abspath('')
bm_tot_uc = pd.DataFrame({'biomass std (%)': (np.array([x.s/x.n for x in bm])*100), 'year':np.int_(years)})
bm_tot_uc.to_excel(file_path + "/../data/biomass_dry_uc.xlsx", index=False)
bmw_tot_uc = pd.DataFrame({'biomass std (%)': (np.array([x.s/x.n for x in bm_w])*100), 'year':np.int_(years)})
bmw_tot_uc.to_excel(file_path + "/../data/biomass_wet_uc.xlsx", index=False)

