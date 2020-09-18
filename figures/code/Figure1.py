# -*- coding: utf-8 -*-

import pandas as pd
import os

file_path = os.path.dirname(os.path.realpath(__file__))

# File uploads - figure1
anthro = (pd.read_excel(file_path + "/../../data/anthropogenic_mass_2015.xlsx", index_col='Year')).iloc[:,:7]
anthro_ext = (pd.read_excel(file_path + "/../../data/anthropogenic_mass_2037.xlsx", index_col='Year')).iloc[:,:7]
biomass_dry = pd.read_excel(file_path + "/../../data/biomass_dry.xlsx")
biomass_dry_uc = pd.read_excel(file_path + "/../../data/biomass_dry_uc.xlsx")

# Adding and subtracting standard deviation 
biomass_dryh = pd.DataFrame({'year': biomass_dry['year'][:95], 'biomass (Tt)': biomass_dry['biomass (Tt)'][:95] + ((biomass_dry['biomass (Tt)'][:95]* biomass_dry_uc['biomass std (%)'][:95])/100)})
biomass_dryl = pd.DataFrame({'year': biomass_dry['year'][:95], 'biomass (Tt)': biomass_dry['biomass (Tt)'][:95] - ((biomass_dry['biomass (Tt)'][:95]* biomass_dry_uc['biomass std (%)'][:95])/100)})

# Initializing with 1900 values 
anthro1900 = [1900,0.002258563,0.016639681,0.011143095,0 ,0.000838412,0.004274367, 0]
anthro = anthro.shift(periods=1)[1:].reset_index()
anthro_ext = anthro_ext.shift(periods=1)[1:].reset_index()
anthro = pd.concat([pd.DataFrame([anthro1900], columns = list(anthro.columns)),anthro])
anthro = pd.concat([anthro, pd.DataFrame([list(anthro_ext.iloc[0])], columns = list(anthro.columns))])

# Plot colors  
c = ['#352a86', '#0870de', '#93552F', '#333333', '#9b111e', '#fdc832', '#969696']  

biomass_dry['biomass (Tt)'] = biomass_dry['biomass (Tt)'].rolling(window=5, min_periods=1).mean()
biomass_dryh['biomass (Tt)'][:89] = biomass_dryh['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()
biomass_dryl['biomass (Tt)'][:89] = biomass_dryl['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()     

# Plotting
ax = anthro.iloc[:, :-1].plot(x='Year', kind='area', legend='reverse', xlim=(1900, 2025), ylim=(0, 1.600), xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], color=c, lw=0)
ax.set_xticklabels([1900, 1920, 1940, 1960, 1980, 2000, 2020], rotation=0, fontsize=6)
ax.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], rotation=0, fontsize=6)           
biomass_dry[:95].plot(x='year',ax=ax, legend=None, color='#006400', lw =1, linestyle='-')                  
biomass_dry[94:97].plot(x='year',ax=ax, legend=None, color='#006400', lw =1, linestyle=':', alpha = 0.5, dashes=(1, 1))                  
biomass_dryh[:90].plot(x='year',ax=ax, legend=None, color='#a9ddb5', lw =0.5, linestyle='--')
biomass_dryh[90:95].plot(x='year',ax=ax, legend=None, color='#a9ddb5', lw =0.5, linestyle='--')
biomass_dryl[:90].plot(x='year',ax=ax, legend=None, color='#a9ddb5', lw=0.5, linestyle='--')
biomass_dryl[90:95].plot(x='year',ax=ax, legend=None, color='#a9ddb5', lw=0.5, linestyle='--')
anthro_ext.iloc[:11, :-1].plot(x='Year', ax=ax,kind='area', legend=None, color=c, alpha=0.5,lw=0)
ax.set_xlabel('year', fontsize=7)
ax.set_ylabel('dry weight (Teratonnes)', fontsize=7)
ax.text(1975, 0.325, 'anthropogenic\nmass', ha = 'center', size=7)
ax.text(1975, 1.170, 'biomass', ha = 'center', size=7)
ax.axvline(x=2020, ymax=1115.0/1600, linestyle='--', linewidth=0.4, color='k', alpha=0.5)
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles[6:12]), reversed(labels[6:12]), prop={'size': 5.5}, bbox_to_anchor=(0, 0.780/1.750), loc="upper left",frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.text(2009.8, 1.17, '2020' + r'$\pm$' + '6', size=6)
ax.scatter(2020, 1.119, color='black', s=12, zorder=10)
ax.figure.set_figheight(2.3)
ax.figure.set_figwidth(3.5)
file_out_name = file_path + '/../output/figure1'
ax.figure.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
ax.figure.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)
ax.figure.savefig(file_out_name+'.pdf', bbox_inches='tight', pad_inches = 0.05)