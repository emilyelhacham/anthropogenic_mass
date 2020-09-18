#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load dependencies 
import numpy as np
import pandas as pd
from scipy.stats.mstats import gmean


# # Wet weight calculation
# 
# 
# ## Biomass wet weight 
# 
# The biomass wet weight is derived based on the dry weight using a conversion factor  (see below, the ratio between the wet and dry weights). The factor is based on the wet to dry mass ratio of trees, which represent the majority of the global biomass. It is composed of the corresponding factors of the three main tree compartments: roots, stem and leaves. The three factors were derived according to wet mass records, moisture content data and dry matter content measurements respectively.
# 
# $\begin{equation*}Conversion\,factor\,(\alpha) = \frac{Mwet}{Mdry} \end{equation*}$
# 
# ### Stem
# 
# The stem wet to dry mass conversion factor is computed based on a dataset of the average green wood moisture content (MC) of 62 tree species by [Glass et al.](https://www.fs.usda.gov/treesearch/pubs/37428).
# 
# $\begin{equation*}Moisture\,Content\,(MC) = \frac{Mwet-Mdry}{Mdry} = \alpha -1  \end{equation*}$
# 
# The dataset contains the MC values of sapwood and heartwood of each species (classified into softwood or hardwood). Here is a sample: 

# In[2]:


#Load trees MC data
wood_MC = pd.read_excel("wood_MC.xlsx")
wood_MC.head()


# Our best estimate of trees MC value is the geometric mean of the MC values of all available species. 
# The best estimate of each species MC value is based on the mean of the respective sapwood and heartwood MC values, assuming the mass ratio between heartwood and sapwood is 1:1.

# In[3]:


mc_tot = gmean((wood_MC['Heartwood MC%'] + wood_MC['Sapwood MC%'])/2).round(-1)
#MC units are (%)


# We now convert the derived MC value to dry to wet mass conversion factor according to the above formula (i.e. dividing the MC% values by 100% and adding 1). This results in our best estimate of the overall wood dry to wet mass factor:

# In[4]:


stem_d2w = mc_tot/100 + 1 

print 'Our best estimate of the stem dry to wet mass conversion factor is ' + str(stem_d2w)


# ### Roots
# 
# The roots mass conversion factor is calculated according to 30 wet and dry roots mass measurements of total of 4 tree species by [Guo et al.](https://doi.org/10.1007/s11104-013-1710-4).<br>Here is a sample from Guo et al.:

# In[5]:


#Load roots records
roots = pd.read_excel("roots_meas.xlsx")
roots.head()


# Our best estimate of the conversion factor is the geometric mean of all calculated conversion factors of all samples:

# In[6]:


roots_d2w = gmean((roots['Fresh Weight (g)']/ roots['Dry Weight (g)'])).round(1)

print 'Our best estimate of the roots dry to wet mass conversion factor is ' + str(roots_d2w)


# ### Leaves
# 
# The dry to wet mass conversion factor of leaves is derived based on dry matter content (DMC) datasets ([Boucher et al.](https://doi.org/10.1111/1365-2435.12034), [Dahlin et al.](https://doi.org/10.1073/pnas.1215513110), [Loveys et al.](https://doi.org/10.1046/j.1365-2486.2003.00611.x), [Messier et al.](https://doi.org/10.1111/j.1461-0248.2010.01476.x), [Michaletz et al.](https://doi.org/10.1139/x06-158), Sheremetev et al.), obtained via [TryDB](https://doi.org/10.1111/j.1365-2486.2011.02451.x). The datasets include DMC measurements of a total of 218 plant species. For each species, the geometric mean DMC value was calculated. 
# 
# $\begin{equation*}Dry\,Matter\,Content\,(DMC) = \frac{Mdry}{Mwet} = \frac{1}{\alpha} \end{equation*}$
# 
# Here is a sample:

# In[7]:


leaves_DMC = pd.read_excel("leaves_DMC.xlsx")
leaves_DMC.head()


# Our best estimate of the leaves DMC is the geometric mean of all values. The wet to dry mass conversion factor is then derived according to the formula, as follows:

# In[8]:


leaves_d2w = (1/ gmean(leaves_DMC['DMC'])).round(1)
print 'Our best estimate of the leaves dry to wet mass conversion factor is ' + str(leaves_d2w)


# ### Integrated factor
# 
# After deriving the factors of the three tree compartments, the next step is to calculate the integrated conversion factor to be used throughout this study. 
# To derive it, we divide the global plants wet mass by the dry mass. <br> The global plants dry weight is calculated as the sum of the global dry mass of the three plant compartments: stem, roots and leaves, obtained from [Bar-On et al.](https://doi.org/10.1073/pnas.1711842115). The global plant wet mass is computed by first multiplying each plant compartment global dry mass by its corresponding conversion factor. <br> Later, those are summed together to obtain the overall global plants wet mass:
# 

# In[9]:


#Global dry mass (Gt) of the three tree compartments, source: [Bar-On et al.] 
d_weights = {'stem': 600, 'roots': 300, 'leaves': 30}

d2w = (stem_d2w * d_weights['stem'] + roots_d2w * d_weights['roots'] + leaves_d2w * d_weights['leaves'])/ sum(d_weights.values())

print 'Our best estimate of the biomass dry to wet mass conversion factor is ' + str(d2w)

