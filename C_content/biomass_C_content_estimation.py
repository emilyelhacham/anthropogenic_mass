#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load dependencies 
import numpy as np
import pandas as pd
from uncertainties import ufloat
from uncertainties import unumpy


# # Biomass C content estimation
# 
# Biomass is presented in the paper on a dry-weight basis. As part of the biomass calculation, we converted biomass in carbon-weight basis to dry-weight basis by multiplying by a conversion factor. 
# 
# ## Conversion factor calculation  
# 
# The conversion factor was calculated based on C content estimates of the different plant compartments (leaves, stems and roots) of different biomes, from [Tang et al.](https://doi.org/10.1073/pnas.1700295114) (units: (mg/g)). 

# In[2]:


# Upload C content data from Tang et al., units [mg/g]
c_content = pd.read_excel("C_content_Tang.xlsx")
c_content


# In[3]:


# Save parameters to unumpy arrays 
cleaf = unumpy.uarray(list(c_content['leaf']), list(c_content['leaf std']))
cstem = unumpy.uarray(list(c_content['stem'].fillna(0)), list(c_content['stem std'].fillna(0)))
croot = unumpy.uarray(list(c_content['root']), list(c_content['root std']))


# For each biome, we calculate the weighted average C content according to the mass fraction of each plant compartment. Information on plants compartmental mass composition was obtained from [Poorter et al.](https://nph.onlinelibrary.wiley.com/doi/full/10.1111/j.1469-8137.2011.03952.x). 

# In[4]:


# Upload compartmental mass composition, from Poorter et al., classified according to Tang et al. biomes   
compart_comp = pd.read_excel("compartment_comp_Poorter.xlsx")
compart_comp


# In[5]:


# Save parameters to unumpy arrays 
fleaf = unumpy.uarray(list(compart_comp['leaf']), list(compart_comp['leaf std']))
fstem = unumpy.uarray(list(compart_comp['stem'].fillna(0)), list(compart_comp['stem std'].fillna(0)))
froot = unumpy.uarray(list(compart_comp['root']), list(compart_comp['root std']))


# In[6]:


# Calculate the weighted average for each biome 
cbiome = (cleaf*fleaf)+(cstem*fstem)+(croot*froot) 


# Next, we calculate the plants conversion factor, according to the mass fraction of each biome, which was calculated by the corresponding mass of each of the biome categories, derived from [Erb et al.](https://doi.org/10.1038/nature25138).

# In[7]:


# Upload biomes biomass, from Erb et al., classified according to Tang et al. biomes  
mbiome = pd.read_excel('biome_mass_Erb.xlsx')
mbiome


# In[8]:


# Save to unumpy array 
mbiomes = unumpy.uarray(list(mbiome['biomass [Gt C]']), list(mbiome['biomass std']))

# Calculate the overall conversion factor 
cplants_factor = 1000/np.sum((cbiome* (mbiomes/np.sum(mbiomes))))


# In the overall carbon-weight to dry-weight conversion factor, we also accounted the C content of non-plant biomass, which was based on estimates from [Heldal et al.](https://aem.asm.org/content/50/5/1251.short) and [von Stockar](https://www.sciencedirect.com/science/article/pii/S0005272899000651). We used the current estimate of non-plant biomass fraction - about 10% of the total biomass, according to [Bar-On et al.](https://doi.org/10.1073/pnas.1711842115) and [updates](https://doi.org/10.1038/s41561-018-0221-6).

# In[9]:


# Upload non plant C content data, units [g/g]  
cnon_plant = pd.read_excel('C_content_non_plant.xlsx')
cnon_plant


# In[10]:


# Calculate conversion factors 
cnon_plant_factor = ufloat(np.average(cnon_plant['C content']) ,np.std(cnon_plant['C content'], ddof = 1))
cfactor = (cplants_factor*0.9) +(0.1*(1/cnon_plant_factor))
cfactor
print 'Our best estimate of the C content conversion factor is: ' + "%.2f" % (cfactor.n) + ', with uncertainty (±1 standard deviation): ' + "%.2f" % (cfactor.s) 

