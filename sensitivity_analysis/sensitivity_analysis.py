#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load dependencies 
import numpy as np
import pandas as pd
import os


# # Sensitivity analysis of the anthropogenic mass definition
# 
# In this study, anthropogenic mass is defined as the mass embedded in inanimate solid objects made by humans, that were not yet demolished or taken out of service. This definition is supported by the scientific field of industrial ecology and used by bureaus of statistics. Other definitions can be proposed. Here we present their calculations.

# In[2]:


# Upload our anthropogenic mass and biomass estimates 
anthropogenic_mass = pd.concat([pd.read_excel("../data/anthropogenic_mass_2015.xlsx").iloc[:,:7],pd.read_excel("../data/anthropogenic_mass_2037.xlsx").iloc[1:6,:7]]).reset_index(drop=True)
anthropogenic_mass['anthropogenic_mass'] = anthropogenic_mass.iloc[:,1:].sum(axis=1)
biomass = pd.read_excel("../data/biomass_dry.xlsx")

# Fill yearly values
bm = np.empty(0)
for i in xrange (5):
    bm = np.append(bm,np.linspace(biomass.iloc[90+i,0],biomass.iloc[90+i+1,0],int(biomass.iloc[i+91,1] - biomass.iloc[i+90,1] +1))[:-1])
biomass = pd.DataFrame({'Year': xrange(biomass.iloc[0,1], biomass.iloc[-1,1]+1), 'biomass(Tt)': list(biomass.iloc[:90,0]) +list(bm)+list(biomass.iloc[95:,0])}, columns = ['biomass(Tt)','Year'])


# ## Include humans under anthropogenic mass instead of under biomass 
# 
# The mass of the human population since 1900 was obtained from [Krausmann et al., 2018](http://dx.doi.org/10.1016/j.gloenvcha.2018.07.003) and was converted to a dry-weight basis by multiplying by 0.3 (assuming water comprises 70% of the human body’s mass).

# In[3]:


# Upload the mass of human population from Krausmann et al., units [Gigatonnes] 
human = pd.read_excel("human_livestock_Krausmann.xlsx").iloc[:,[0,1]]
# Convert to dry weight basis and units of Teratonnes
human.iloc[:,1] = human.iloc[:,1]* 0.3 /1000 
human.head()


# In[4]:


# Extrapolate till 2020
factor = (human.iloc[-5:, 1] / human.shift(1).iloc[-5:, 1]).mean()
human_ext = pd.DataFrame({'Year': xrange(2015, 2021), 'Humans':[human.iloc[-1, 1] * (factor ** i) for i in range(6)]}, columns = ['Year', 'Humans'])
human = pd.concat([human, human_ext.iloc[1:, :]]).reset_index(drop=True)


# The mass of the human population was then subtracted from the biomass estimate and added to the anthropogenic mass estimate.

# In[5]:


biomass_human = biomass[:121].iloc[:,0] - human.iloc[:,1]
anthropogenic_mass_human = anthropogenic_mass[:121].iloc[:,7] + human.iloc[:,1]


# ## Include livestock under anthropogenic mass instead of under biomass 
# 
# The mass of the livestock since 1900 was obtained from [Krausmann et al., 2018](http://dx.doi.org/10.1016/j.gloenvcha.2018.07.003) and was converted to a dry-weight basis by multiplying by 0.3 (assuming water comprises 70% of the mass of livestock).

# In[6]:


# Upload the mass of livestock from Krausmann et al., units [Gigatonnes] 
livestock = pd.read_excel("human_livestock_Krausmann.xlsx").iloc[:,[0,2]]

# Convert to dry weight basis and units of Teratonnes
livestock.iloc[:,1] = livestock.iloc[:,1]* 0.3 /1000
livestock.head()


# In[7]:


# Extrapolate till 2020
factor = (livestock.iloc[-5:, 1] / livestock.shift(1).iloc[-5:, 1]).mean()
livestock_ext = pd.DataFrame({'Year': xrange(2015, 2021), 'Livestock':[livestock.iloc[-1, 1] * (factor ** i) for i in range(6)]}, columns = ['Year', 'Livestock'])
livestock = pd.concat([livestock, livestock_ext.iloc[1:, :]]).reset_index(drop=True)


# The livestock mass was subtracted from the biomass estimate and added to the anthropogenic mass estimate.

# In[8]:


biomass_livestock = biomass[:121].iloc[:,0] - livestock.iloc[:,1]
anthropogenic_mass_livestock = anthropogenic_mass[:121].iloc[:,7] + livestock.iloc[:,1]


# ## Exclude industrial roundwood mass from the anthropogenic mass 
# 
# The industrial roundwood mass since 1900 was obtained from [Wiedenhofer et al., 2019](http://dx.doi.org/10.1016/j.ecolecon.2018.09.010).

# In[9]:


# Upload the mass of industrial roundwood from Wiedenhofer et al., units [Gigatonnes] 
wood = pd.read_excel("roundwood_Wiedenhofer.xlsx") 
wood.head()


# In[10]:


# Sum the solidwood and paper estimates and convert to units of Teratonnes
wood = pd.DataFrame({'Year': wood.iloc[:,0], 'Roundwood': (wood["Solidwood"] + wood["Paper"])/1000}, columns = ['Year', 'Roundwood'])

# Extrapolate till 2020
factor = (wood.iloc[-5:, 1] / wood.shift(1).iloc[-5:, 1]).mean()
wood_ext = pd.DataFrame({'Year': xrange(2014, 2021), 'Roundwood':[wood.iloc[-1, 1] * (factor ** i) for i in range(7)]}, columns = ['Year', 'Roundwood'])
wood = pd.concat([wood, wood_ext.iloc[1:, :]]).reset_index(drop=True)


# We then subtract the industrial roundwood from the anthropogenic mass estimate.

# In[11]:


anthropogenic_mass_wood = anthropogenic_mass[:121].iloc[:,7] - wood.iloc[:,1]


# ## Include mass of crops and agroforestry under anthropogenic mass instead of under biomass
# 
# To calculate the mass of crops and agroforestry (i.e., trees integrated in agricultural settings/landscapes), we mostly relied on the work by [Zomer et al.](http://dx.doi.org/10.1038/srep29987). We first estimated the area of the agricultural land, and then multiplied it by the corresponding biomass density
# 
# To derive the agriculture area since 1900, we use the 2000 area estimate by [Zomer et al., 2016](http://dx.doi.org/10.1038/srep29987) and as an approximation, assume it behaves similarly to the cropland area.
# The cropland area estimates were obtained from [Goldewijk et al., 2017](http://dx.doi.org/10.5194/essd-9-927-2017) (Table S3), HYDE 3.2.

# In[12]:


# Zomer et al. total agricultural area in 2000, Units [km^2] 
agr_area2000= 22168929

# convert to units of Mkm^2 
agr_area2000= agr_area2000/1e6

# Upload the cropland area from HYDE3.2, units [Mkm^2] 
crop_area = pd.read_excel("cropland_HYDE32.xlsx")
crop_area.head()


# In[13]:


# Derive the agricultural area since 1900
agr_area = pd.DataFrame({'Year': crop_area.iloc[:,0], 'agr_area': crop_area.iloc[:,1]/crop_area.iloc[10,1] * agr_area2000}, columns = ['Year', 'agr_area'])

# Convert to units of ha
agr_area.iloc[:,1] = agr_area.iloc[:,1]* 1e8 


# Next, we derive the trend in the mass density between 2000-2010, using the two corresponding estimates by [Zomer et al.](http://dx.doi.org/10.1038/srep29987):

# In[14]:


# Upload the mass densities from Zomer et al., units [tC/ha] 
agr_den = pd.read_excel("agr_density_Zomer.xlsx")

# Calculate the linear density trend 
den_trend = np.polyfit(agr_den.iloc[:,0],agr_den.iloc[:,1], 1)[0]


# We now multiply the agricultural area by the corresponding density, assuming the density trend remains constant, to obtain the mass of crops and agroforestry.

# In[15]:


# Estimate the mass density since 1900
agr_densities = pd.DataFrame({'Year': crop_area.iloc[:,0],'Density': [agr_den.iloc[0,1] - (den_trend * 10* (i+1)) for i in range(10)][::-1] + [agr_den.iloc[0,1] + (den_trend * i) for i in range(21)]},columns = ['Year', 'Density']) 

# Calculate the mass on agriculture land since 1900
agr_mass = pd.DataFrame({'Year': crop_area.iloc[:,0], 'agr_mass': (agr_area.iloc[:,1])* agr_densities.iloc[:,1]}, columns = ['Year', 'agr_mass'])

CFACTOR = 2.25

# Convert to units of Teratonnes of dry weight basis
agr_mass.iloc[:,1] = agr_mass.iloc[:,1]* CFACTOR/1e12


# The mass of crops and agroforestry was subtracted from the biomass estimate and added to the anthropogenic mass estimate.

# In[16]:


bm_df = np.empty(0)
for i in xrange (10):
    bm_df = np.append(bm_df,np.linspace(agr_mass.iloc[i,1],agr_mass.iloc[i+1,1],int(agr_mass.iloc[i+1,0] - agr_mass.iloc[i,0] +1))[:-1])
biomass_agr = biomass[:121].iloc[:,0] - (np.concatenate([bm_df,agr_mass.iloc[10:,1]]))
anthropogenic_mass_agr = anthropogenic_mass.iloc[:121,7] + (np.concatenate([bm_df,agr_mass.iloc[10:,1]]))


# ## Add atmospheric anthropogenic CO<sub>2</sub> stocks to the anthropogenic mass  
# To estimate the stock of anthropogenic CO<sub>2</sub> mass over the studied period, we subtracted the pre-industrial CO<sub>2</sub> mass from the annual mean CO<sub>2</sub> stocks since 1900. 
# 
# Annual atmospheric CO<sub>2</sub> concentrations from 1959-2019 were obtained from [NOAA/ESRL](https://www.esrl.noaa.gov/gmd/ccgg/trends/) (Dr. Pieter Tans; Mauna Loa Observatory, Hawaii) and the [Scripps Institution of Oceanography](https://scrippsco2.ucsd.edu) (Dr. Ralph Keeling). 

# In[17]:


# Upload CO2 concentrations since 1959, units [ppm]
CO2 = pd.read_excel('CO2_NOAA_SOI.xlsx')
CO2.head()


# Prior estimates, based on ice cores, were obtained from [MacFarling Meure et al., 2006](https://doi.org/10.1029/2006GL026152); multiple records available for the same year were averaged.

# In[18]:


# Upload CO2 concentrations since 1899, units [ppm]
CO2_p = pd.read_excel('CO2_MacFarling_Meure.xlsx')
CO2_p.iloc[:,1] = np.floor(CO2_p.iloc[:,1])
CO2_p = CO2_p.groupby(['CO2 gas age years AD']).mean().reset_index()
CO2_p.head()


# We then convert the concentration estimates to mass stocks of Gigatonnes CO<sub>2</sub>. This is done by first using a conversion factor from ppm CO<sub>2</sub> to Gigatonnes C, obtained from [Friedlingstein et al., 2019](http://doi.org/10.5194/essd-11-1783-2019). Later we convert to Gigatonnes CO<sub>2</sub> by multiplying by the ratio of the molecular weights:

# In[19]:


# Combine the two time periods
CO2 = pd.DataFrame({'Year': list(CO2_p.iloc[:,0]) + list(CO2.iloc[:,0]), 'CO2': list(CO2_p.iloc[:,1])+ list(CO2.iloc[:,1])}, columns = ['Year', 'CO2'])

# Convert to Gigatonnes CO2
conv_factor1 = 2.124
conv_factor2 = 44.01/12.011
CO2.iloc[:,1] = CO2.iloc[:,1]* conv_factor1* conv_factor2


# We now subtract the CO<sub>2</sub> pre-industrial stocks, which derived based on the [IPCC](https://archive.ipcc.ch/ipccreports/tar/wg1/016.htm) concentration estimate of about 280 ppm.

# In[20]:


# Pre-industrial CO2 concentration according to the IPCC, units [ppm]
Pre_ind = 280

# Convert to Gigatonnes CO2 
Pre_ind = Pre_ind* conv_factor1* conv_factor2

# Reduce from the CO2 stocks since 1900
CO2.iloc[:,1] = CO2.iloc[:,1] - Pre_ind


# The atmospheric anthropogenic CO<sub>2</sub> mass was then added to the anthropogenic mass estimate.

# In[21]:


am_CO2 = np.empty(0)
for i in xrange (30):
    am_CO2 = np.append(am_CO2,np.linspace(CO2.iloc[i,1],CO2.iloc[i+1,1],int(CO2.iloc[i+1,0] - CO2.iloc[i,0] +1))[:-1])
# Add to the anthropogenic mass estimate and convert to Teratonnes 
anthropogenic_mass_CO2 = anthropogenic_mass[:120].iloc[:,7] + (np.concatenate([am_CO2[1:],CO2.iloc[30:,1]]))/1000


# ## Add civil engineering earthworks, dredging and waste/overburden from metal and mineral production to the anthropogenic mass 
# 
# The anthropogenic mass definition is composed only of the current in-use human-made mass. In addition to this mass, humanity moves and extracts material not intended for usage, for example, waste or overburden from mineral extraction, civil engineering excavations and dredging.
# 
# Our estimation for the yearly addition resulting of these actions is mostly based on a recent study by [Cooper et al. 2018](http://dx.doi.org/10.1177/2053019618800234), with updates to complement our anthropogenic mass estimation and avoid double counting. We include four groups: dredging, civil engineering earthworks, waste/ overburden resulted from mineral/metal or coal production.

# ### dredging 
# The mass associated with dredging, since 1925, was obtained from [Cooper et al.](http://dx.doi.org/10.1177/2053019618800234), SI table1.

# In[22]:


# Upload dredging data from Cooper et al., units [Mt/y]
dredging = pd.read_excel("excavations_Cooper.xlsx").iloc[:,[0,1]]

# Convert to units of Teratonnes/year
dredging['dredging'] = dredging.iloc[:,1]/1e6


# We then extrapolate the estimate from 1925 till 1900, based on the first five years, assuming exponential growth.

# In[23]:


# Extrapolate the estimate from 1925 till 1900, based on the first five years, assuming exponential growth
factor = (dredging.shift(-1).iloc[:5, 1] / dredging.iloc[:5, 1]).mean()
dredging = pd.DataFrame({'Year': xrange(1900, 2016),'dredging': [dredging.iloc[0, 1] / (factor ** i) for i in range(26)][::-1] + list(dredging.iloc[1:, 1])}, columns = ['Year', 'dredging'])


# ### waste/ overburden from coal production 
# The waste/ overburden from coal production were adopted from [Cooper et al.](http://dx.doi.org/10.1177/2053019618800234), SI table1.

# In[24]:


# Upload waste/ overburden from coal production data from Cooper et al. SI table1, units [Mt/y]
coal_over = pd.read_excel("excavations_Cooper.xlsx").iloc[:,[0,2]]

# Convert to units of Teratonnes/year
coal_over['overburden/ waste\nfrom coal production'] = coal_over.iloc[:,1]/1e6


# In[25]:


# Extrapolate the estimate from 1925 till 1900, based on the first five years, assuming exponential growth
factor = (coal_over.shift(-1).iloc[:5, 1] / coal_over.iloc[:5, 1]).mean()
coal_over = pd.DataFrame({'Year': xrange(1900, 2016),'overburden/ waste\nfrom coal production': [coal_over.iloc[0, 1] / (factor ** i) for i in range(26)][::-1] + list(coal_over.iloc[1:, 1])}, columns = ['Year', 'overburden/ waste\nfrom coal production'])


# ### civil engineering earthworks
# 
# The mass of civil engineering earthworks was derived by multiplying the mass of used cement and aggregates by a factor of 2, following the approach presented in [Cooper et al.](http://dx.doi.org/10.1177/2053019618800234). 
# 
# To estimate the mass of cement and aggregates used each year, we first calculate the net addition to stocks for the aggregates, concrete and asphalt categories. Asphalt values were multiplied by 0.95 to represent the fraction of aggregates.

# In[26]:


# Calculating the yearly net additions to stocks for the aggregates and concrete and asphalt categories 
nas = (anthropogenic_mass.iloc[:,[1,2]] - anthropogenic_mass.shift(1).iloc[:,[1,2]])
asphalt = 0.95*(anthropogenic_mass.iloc[:,[4]] - anthropogenic_mass.shift(1).iloc[:,[4]])

# Summing all additions
nas = (nas.sum(axis=1) + np.array(list(asphalt.iloc[:,0]))).fillna(0)


# To approximate the mass of aggregates and cement used each year, we add to the yearly net additions to stocks the yearly waste of these categories.
# The waste here includes the end-of-life, construction and re-manufacturing wastes, in addition recycling is considered in the calculation. Thus the approximation of the used cement and aggregates might be slightly high.

# In[27]:


# Upload the annual waste of the aggregates, concrete and asphalt categories, units [Gigatonnes/t] 
waste = pd.read_excel("waste_Wiedenhofer.xlsx")

# Sum the waste flows, converted to Teratonnes/year
waste = waste.iloc[:,1:4].sum(axis=1)/1000 + np.array(list(waste.iloc[:,4]*0.95))/1000


# We then multiplied the outcome by a factor of 2, to obtain the annual mass of earthwork. 

# In[28]:


earthwork = 2 * (nas[:100] + waste[:100])


# ### waste/overburden resulted from mineral/metal production
# To estimate the amount of waste/overburden resulted from mineral/metal production, we used [Cooper et al.](http://dx.doi.org/10.1177/2053019618800234) values, which combined the mineral/metal production and the associated waste/overburden. 
# 
# To avoid double counting, we interpolated their mineral/metal production for all years (using the provided estimates for selected years), based on exponential fit.

# In[29]:


# Upload waste/overburden resulted from mineral/metal production from Cooper et al., units [Mt/y]
m_over = pd.read_excel("excavations_Cooper.xlsx").iloc[:,[0,3]]
m_over.head()


# To avoid double counting with our anthropogenic mass estimate, we subtracted from this combined estimate the mineral/metal production. 
# This was performed by interpolating the production for all years, according the provided production estimates for selected years, using exponential fit.

# In[30]:


# Upload metal/mineral production estimates from Cooper et al., units [tonnes/y]
m_prod = pd.read_excel("mprod_Cooper_full.xlsx")
m_prod.head()


# In[31]:


# Sum all and convert to Megatonnes/year 
m_prod = pd.DataFrame({'Year':list(m_prod)[1:], 'Production': list(m_prod.sum()[1:]/1e6)}, columns = ['Year', 'Production'])

# Interpolate the yearly production estimates from 1925 till 1976 using exponential fit, according to the years of interest
a, b = np.polyfit(m_prod.iloc[:3,0], np.log(m_prod.iloc[:3,1]), 1)
x = np.linspace(1925,1976,52)
m_prod= np.exp(b)* np.exp(a*x)


# In[32]:


# Estimate the waste/overburden only and convert to Teratonnes   
m_over = (m_over.iloc[:52,1] - m_prod)/1e6


# In[33]:


# Extrapolate the estimate from 1925 to 1900
factor = (np.array(m_over[1:6])/ np.array(m_over[:5])).mean()
m_over = pd.DataFrame({'Year': xrange(1900, 1977), 'm_over':[m_over[0] / (factor ** i) for i in range(26)][::-1]+ list(m_over[1:])}, columns = ['Year', 'm_over'])


# ### overall mass associated with civil engineering earthworks, dredging and waste/overburden from metal and mineral production 
# 
# To calculate the mass excavated/moved, we sum the four contributions: dredging, civil engineering earthworks, waste/ overburden resulted from mineral/metal and coal production.  

# In[34]:


excavations = np.array(list(dredging.iloc[:77,1])) + np.array(list(coal_over.iloc[:77,1])) + np.array(list(earthwork[:77])) + np.array(list(m_over.iloc[:,1]))


# We add the accumulated excavated/moved mass to the anthropogenic mass estimate.  

# In[35]:


anthropogenic_mass_exca =  [anthropogenic_mass.iloc[0,7] + excavations[0]]
for i in xrange(76):
    anthropogenic_mass_exca.append((anthropogenic_mass.iloc[:,7] - anthropogenic_mass.iloc[:,7].shift(1))[i+1] + excavations[i+1] + anthropogenic_mass_exca[-1])


# ## Saving anthropogenic mass & biomass data into file

# In[36]:


dic = {'Year': xrange(1900, 2021),
                     'biomass': list(biomass.iloc[:121,0]),
                     'biomass human': list(biomass_human),
                     'biomass livestock': list(biomass_livestock),
                     'biomass agriculture': list(biomass_agr),
                     'anthropogenic mass human': list(anthropogenic_mass_human),
                     'anthropogenic mass livestock': list(anthropogenic_mass_livestock),
                     'anthropogenic mass agriculture': list(anthropogenic_mass_agr),
                     'anthropogenic mass excavations': list(anthropogenic_mass_exca),
                     'anthropogenic mass wood': list(anthropogenic_mass_wood),
                     'anthropogenic mass CO2': list(anthropogenic_mass_CO2)}


# In[37]:


sensitivity = pd.DataFrame({k: pd.Series(l) for k, l in dic.iteritems()}, columns = ['Year', 'biomass','biomass human', 'biomass livestock', 'biomass agriculture','anthropogenic mass human', 'anthropogenic mass livestock', 'anthropogenic mass agriculture','anthropogenic mass excavations', 'anthropogenic mass wood', 'anthropogenic mass CO2']) 
file_path = os.path.abspath('')
writer = pd.ExcelWriter(file_path + "/../data/sensitivity_analysis.xlsx")
sensitivity.to_excel(writer, index=False)
worksheet = writer.sheets['Sheet1']
worksheet.write(0, 11, 'anthropogenic mass values refer to end of year estimates')
writer.save()

