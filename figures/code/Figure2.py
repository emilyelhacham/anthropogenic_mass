# -*- coding: utf-8 -*-

import pandas as pd
import os

file_path = os.path.dirname(os.path.realpath(__file__))

# File uploads - figure2
anthro = (pd.read_excel(file_path + "/../../data/anthropogenic_mass_2015.xlsx", index_col='Year')).iloc[:,:7]
anthro_ext = (pd.read_excel(file_path + "/../../data/anthropogenic_mass_2037.xlsx", index_col='Year')).iloc[:,:7]
biomass_dry = pd.read_excel(file_path + "/../../data/biomass_dry.xlsx")
biomass_dry_uc = pd.read_excel(file_path + "/../../data/biomass_dry_uc.xlsx")
biomass_wet = pd.read_excel(file_path + "/../../data/biomass_wet.xlsx")
biomass_wet_uc = pd.read_excel(file_path + "/../../data/biomass_wet_uc.xlsx")

# Initializing with 1900 values 
anthro1900 = [1900,0.002258563,0.016639681,0.011143095,0 ,0.000838412,0.004274367, 0]
anthro = anthro.shift(periods=1)[1:].reset_index()
anthro_ext = anthro_ext.shift(periods=1)[1:].reset_index()
anthro = pd.concat([pd.DataFrame([anthro1900], columns = list(anthro.columns)),anthro])
anthro = pd.concat([anthro, pd.DataFrame([list(anthro_ext.iloc[0])], columns = list(anthro.columns))])

# Combine categories 
anthro_wet = pd.concat([anthro["Year"],anthro.iloc[:, 1:7].sum(axis=1), anthro.iloc[:, 7]], keys=["Year", 'in-use', 'waste'], axis=1)
anthro_wet_ext = pd.concat([anthro_ext["Year"], anthro_ext.iloc[:, 1:7].sum(axis=1), anthro_ext.iloc[:, 7]], keys=["Year", 'in-use', 'waste'], axis=1)

# Adding and subtracting standard deviation 
biomass_dryh = pd.DataFrame({'year': biomass_dry['year'][:95], 'biomass (Tt)': biomass_dry['biomass (Tt)'][:95] + ((biomass_dry['biomass (Tt)'][:95]* biomass_dry_uc['biomass std (%)'][:95])/100)})
biomass_dryl = pd.DataFrame({'year': biomass_dry['year'][:95], 'biomass (Tt)': biomass_dry['biomass (Tt)'][:95] - ((biomass_dry['biomass (Tt)'][:95]* biomass_dry_uc['biomass std (%)'][:95])/100)})
biomass_weth = pd.DataFrame({'year': biomass_wet['year'][:95], 'biomass (Tt)': biomass_wet['biomass (Tt)'][:95] + ((biomass_wet['biomass (Tt)'][:95]* biomass_wet_uc['biomass std (%)'][:95])/100)})
biomass_wetl = pd.DataFrame({'year': biomass_wet['year'][:95], 'biomass (Tt)': biomass_wet['biomass (Tt)'][:95] - ((biomass_wet['biomass (Tt)'][:95]* biomass_wet_uc['biomass std (%)'][:95])/100)})

biomass_dry['biomass (Tt)'] = biomass_dry['biomass (Tt)'].rolling(window=5, min_periods=1).mean()
biomass_wet['biomass (Tt)'] = biomass_wet['biomass (Tt)'].rolling(window=5, min_periods=1).mean()
biomass_dryh['biomass (Tt)'][:89] = biomass_dryh['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()
biomass_dryl['biomass (Tt)'][:89] = biomass_dryl['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()
biomass_weth['biomass (Tt)'][:89] = biomass_weth['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()
biomass_wetl['biomass (Tt)'][:89] = biomass_wetl['biomass (Tt)'][:89].rolling(window=5, min_periods=1).mean()

# Plotting
bx = anthro_wet.plot(x='Year', legend='reverse', xlim=(1900, 2037), ylim=(0, 3.300),xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0.0, 1.0, 2.0, 3.0],color=['#352a86', '#969696'], kind= 'area', lw=0)
bx.set_xticklabels([1900, 1920, 1940, 1960, 1980, 2000, 2020], rotation=0, fontsize=6)
bx.set_yticklabels([0, 1, 2, 3], rotation=0, fontsize=6)
biomass_wet[:95].plot(x='year', ax=bx, legend=None, color='#006400',lw =1)
biomass_wet[94:].plot(x='year',ax=bx, legend=None, color='#006400', lw =1, linestyle=':', alpha = 0.5, dashes=(0.5, 0.5))                                  
biomass_dry[:95].plot(x='year', ax=bx, legend=None, color='#006400', lw =1)
biomass_dry[94:98].plot(x='year',ax=bx, legend=None, color='#006400', lw =1, linestyle=':', alpha = 0.5,dashes=(0.5, 0.5))                  
biomass_dryh[:90].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw =0.5, linestyle='--',alpha = 0.4,dashes=(2, 4, 2,4))
biomass_dryh[90:95].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw =0.5, linestyle='--',alpha = 0.4,dashes=(2, 4, 2,4))
biomass_dryl[:90].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw=0.5, linestyle='--', alpha = 0.4,dashes=(2, 4, 2,4))
biomass_dryl[90:95].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw=0.5, linestyle='--', alpha = 0.4,dashes=(2, 4, 2,4))
biomass_weth[:90].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw =0.5, linestyle='--',alpha = 0.4)
biomass_weth[90:95].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw =0.5, linestyle='--',alpha = 0.4)
biomass_wetl[:90].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw=0.5, linestyle='--', alpha = 0.4)
biomass_wetl[90:95].plot(x='year',ax=bx, legend=None, color='#a9ddb5', lw=0.5, linestyle='--', alpha = 0.4)
anthro_wet_ext.plot(x='Year', ax=bx, legend=None, color=['#352a86', '#969696'], alpha=0.5, kind= 'area', lw=0)
bx.set_xlabel('year', fontsize=7)
bx.set_ylabel('weight (Teratonnes)', fontsize=7)
bx.text(1915.5, 2.380, 'biomass (wet)', rotation=0, fontsize=7)
bx.text(1915.5, 1.230, 'biomass (dry)', rotation=0, fontsize=7)
bx.axvline(x=2037.5, ymax=2250.0 / 3300, linestyle='--', linewidth=0.5, color='w', alpha=0.7)
bx.axvline(x=2020.0, ymax=1120.0 / 3300, linestyle='--', linewidth=0.5, color='w', alpha=0.7)
bx.axvline(x=2031.5, ymax=2250.0 / 3300, linestyle='--', linewidth=0.5, color='w', alpha=0.7)
bx.axvline(x=2013.0, ymax=1125.0 / 3300, linestyle='--', linewidth=0.5, color='w', alpha=0.7)
handles, labels = bx.get_legend_handles_labels()
bx.legend(reversed(handles[12:14]),['anthropogenic mass waste', 'anthropogenic mass'],prop={'size': 6},bbox_to_anchor=(0, 0.150/4.200), loc="lower left",frameon=False)
bx.spines['right'].set_visible(False)
bx.spines['top'].set_visible(False)
bx.text(2019.7, 2.350, '2037'r'$\pm$'+'10', size=6)
bx.text(2013.6, 2.030, '2031'+r'$\pm$'+'9', size=6)
bx.text(2006.0, 1.250, '2020'+r'$\pm$'+'6', size=6)
bx.text(1995.3, 0.900, '2013'+r'$\pm$'+'5', size=6)
bx.scatter(2037.0, 2.245, color='black', s=6, zorder = 10, clip_on=False)
bx.scatter(2031.5, 2.245, color='black', s=6, zorder = 10)
bx.scatter(2020.0, 1.122, color='black', s=6, zorder = 10)
bx.scatter(2013.0, 1.122, color='black', s=6, zorder = 10)
bx.figure.set_figheight(2.8)
bx.figure.set_figwidth(3.5)
file_out_name = file_path + '/../output/figure2'
bx.figure.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
bx.figure.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)
bx.figure.savefig(file_out_name+'.pdf', bbox_inches='tight', pad_inches = 0.05)