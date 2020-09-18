# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import os 

file_path = os.path.dirname(os.path.realpath(__file__))

# File upload - Extended Data Figure 1
dat = pd.read_excel(file_path + "/../../data/sensitivity_analysis.xlsx").iloc[:,:11]

# Initializing with 1900 values
anthro1900 = [0.03514476,0.03517847,0.06300389, 0.03466347, 0.03101894,0.1580413]
dat.iloc[:,5:11] = dat.iloc[:,5:11].shift(periods=1).reset_index()
dat.iloc[0,5:11] = anthro1900

dat.iloc[:,1:5] = dat.iloc[:,1:5].rolling(window=5, min_periods=1).mean()
dat.iloc[:60,10] = dat.iloc[:60,10].rolling(window=2, min_periods=1).mean()

# Plotting
fig, axes = plt.subplots(nrows=3, ncols=2, sharey=True, sharex = True, figsize=(5.354,5.354))
######Human
dat.iloc[:117,[0,2]].plot(ax=axes[0,0], x= 'Year', legend = None,grid=True,color='#006400', lw = 2, xlim=(1900, 2025), ylim=(0, 1.600), xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
dat.iloc[:117,[0,5]].plot(ax=axes[0,0], x= 'Year', legend = None,grid=True,color='#352a86', kind = 'area', lw =0, zorder=10)
dat.iloc[117:121,[0,2]].plot(x='Year',ax=axes[0,0], legend=None, grid=True, color='#006400', lw =2, linestyle=':', alpha = 0.5, dashes=(0.5, 0.5))                  
dat.iloc[116:121,[0,5]].plot(x='Year',ax=axes[0,0], legend=None, grid=True, color='#9994c2', kind = 'area', lw =0, zorder=10)
axes[0,0].scatter(2020.0, 1.117,color='black', s=12, zorder=10)
axes[0,0].vlines(x=[1920,1940,1960], ymin=1.41, ymax=1.52, color='white', zorder=5, lw=3)
axes[0,0].vlines(x=[1920,1940], ymin=1.28, ymax=1.39, color='white', zorder=5, lw=3)
axes[0,0].text(2005.8, 1.22, '2020',size=7)
axes[0,0].text(1902.0, 1.30, 'including humans under\nanthropogenic mass',size=7,zorder=10)
axes[0,0].set_ylabel ('weight (Teratonnes)', fontsize=7)
axes[0,0].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], rotation=0, fontsize=6)
axes[0,0].tick_params(axis='both', which='minor', bottom=False, top=False,  labelbottom=False, right=False, left=False, labelleft=False)
######Livestock
dat.iloc[:117,[0,3]].plot(ax=axes[0,1], x= 'Year', legend = None,grid=True,color='#006400', lw = 2, xlim=(1900, 2025), ylim=(0, 1.600), xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
dat.iloc[:117,[0,6]].plot(ax=axes[0,1], x= 'Year', legend = None,grid=True,color='#352a86',kind = 'area', lw =0,zorder = 10)
dat.iloc[117:121,[0,3]].plot(x='Year',ax=axes[0,1], legend=None, grid=True, color='#006400', lw =2, linestyle=':', alpha = 0.5, dashes=(0.5, 0.5))                  
dat.iloc[116:121,[0,6]].plot(x='Year',ax=axes[0,1], legend=None, grid=True, color='#9994c2', kind = 'area', lw =0,zorder = 10)
axes[0,1].scatter(2020.0, 1.117,color='black', s=12, zorder=10)
axes[0,1].vlines(x=[1920,1940,1960], ymin=1.41, ymax=1.52, color='white', zorder=5, lw=3)
axes[0,1].vlines(x=[1920,1940], ymin=1.28, ymax=1.39, color='white', zorder=5, lw=3)
axes[0,1].text(2005.8, 1.22, '2020',size=7)
axes[0,1].text(1902.0, 1.30, 'including livestock under\nanthropogenic mass',size=7,zorder=10)
axes[0,1].tick_params(axis='both', which='minor', bottom=False, top=False,  labelbottom=False, right=False, left=False, labelleft=False)
######Agriculture
dat.iloc[:115,[0,4]].plot(ax=axes[1,0], x= 'Year', legend = None,grid=True,color='#006400', lw = 2, xlim=(1900, 2025), ylim=(0, 1.600), xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
dat.iloc[:115,[0,7]].plot(ax=axes[1,0], x= 'Year', legend = None,grid=True,color='#352a86',kind = 'area', lw =0, zorder = 10)
axes[1,0].scatter(2014.0, 1.01,color='black', s=12, zorder=10)
axes[1,0].text(1999.8, 1.107, '2014',size=7)
axes[1,0].vlines(x=[1920,1940,1960,1980,2000], ymin=1.41, ymax=1.52, color='white', zorder=5, lw=3)
axes[1,0].text(1902.0, 1.30, 'including crops and agroforestry under\nanthropogenic mass',size=7, zorder=10)
axes[1,0].vlines(x=[1920,1940], ymin=1.28, ymax=1.39, color='white', zorder=5, lw=3)
axes[1,0].set_ylabel ('weight (Teratonnes)', fontsize=7)
axes[1,0].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], rotation=0, fontsize=6)
axes[1,0].tick_params(axis='both', which='minor', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
######Sediments 
dat.iloc[:76,[0,1]].plot(ax=axes[1,1], x= 'Year', legend = None, grid=True, color='#006400', lw = 2)
dat.iloc[:76,[0,8]].plot(ax=axes[1,1], x= 'Year', legend = None, grid=True, color='#352a86',kind = 'area',lw =0, zorder = 10)
axes[1,1].text(1963.0, 1.21, '1975', size=7)
axes[1,1].vlines(x=[1920,1940,1960,1980,2000], ymin=1.31, ymax=1.59, color='white', zorder=5, lw=3)
axes[1,1].vlines(x=[1920,1940], ymin=1.21, ymax=1.59, color='white', zorder=5, lw=3)
axes[1,1].hlines(y=1.4, xmin=1901.1, xmax=2019.8, color='white', zorder=5, lw=3)
axes[1,1].text(1902.0, 1.25, 'adding earthworks, dredging, overburden\nfrom mineral and metal production to the\nanthropogenic mass',size=7,zorder=10)
axes[1,1].scatter(1975, 1.102, color='black', s=12, zorder = 10)
axes[1,1].tick_params(axis='both', which='minor', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
######Wood 
dat.iloc[:117,[0,1]].plot(ax=axes[2,0], x= 'Year', legend = None,grid=True,color='#006400', lw = 2, xlim=(1900, 2025), ylim=(0, 1.600), xticks=[1900, 1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
dat.iloc[:117,[0,9]].plot(ax=axes[2,0], x= 'Year', legend = None,grid=True,color='#352a86', kind = 'area', lw =0, zorder = 10)
dat.iloc[117:121,[0,1]].plot(x='Year',ax=axes[2,0], legend=None, grid=True, color='#006400', lw =2, linestyle=':', alpha = 0.5, dashes=(0.5, 0.5))                  
dat.iloc[116:121,[0,9]].plot(x='Year',ax=axes[2,0], legend=None, grid=True, color='#9994c2', kind = 'area', lw =0, zorder = 10)
axes[2,0].scatter(2020.0, 1.115,color='black', s=12, zorder=10)
axes[2,0].text(2005.8, 1.20, '2020',size=7)
axes[2,0].vlines(x=[1920,1940,1960,1980], ymin=1.41, ymax=1.52, color='white', zorder=5, lw=3)
axes[2,0].vlines(x=[1920,1940], ymin=1.28, ymax=1.39, color='white', zorder=5, lw=3)
axes[2,0].text(1902.0, 1.30, 'excluding roundwood from the\nanthropogenic mass',size=7,zorder=10)
axes[2,0].set_xlabel ('year', fontsize=7)
axes[2,0].set_xticklabels([1900, 1920, 1940, 1960, 1980, 2000, 2020], rotation=0, fontsize=6)
axes[2,0].set_ylabel ('weight (Teratonnes)', fontsize=7)
axes[2,0].set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6], rotation=0, fontsize=6)
axes[2,0].tick_params(axis='both', which='minor', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
######CO2 
dat.iloc[:97,[0,1]].plot(ax=axes[2,1], x= 'Year', legend = None, grid=True, color='#006400', lw = 2)
dat.iloc[:97,[0,10]].plot(ax=axes[2,1], x= 'Year', legend = None, grid=True, color='#352a86', kind = 'area',lw =0, zorder = 10)
axes[2,1].text(1980.0, 1.22, '1996', size=7)
axes[2,1].vlines(x=[1920,1940,1960,1980,2000,2020], ymin=1.41, ymax=1.52, color='white', zorder=5, lw=3)
axes[2,1].vlines(x=[1920,1940,1960], ymin=1.28, ymax=1.39, color='white', zorder=5, lw=3)
axes[2,1].text(1902.0, 1.30, 'adding atmospheric anthropogenic '+r'$CO_2$'+ ' to \nthe anthropogenic mass',size=7,zorder=10)
axes[2,1].scatter(1996, 1.116, color='black', s=12, zorder = 10)
axes[2,1].set_xlabel ('year', fontsize=7)
axes[2,1].set_xticklabels([1900, 1920, 1940, 1960, 1980, 2000, 2020], rotation=0, fontsize=6)
axes[2,1].tick_params(axis='both', which='minor', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
######
fig.tight_layout()
plt.text(0.025, 0.94, 'a', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
plt.text(0.025, 0.63, 'c', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
plt.text(0.025, 0.32, 'e', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
plt.text(0.525, 0.94, 'b', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
plt.text(0.525, 0.63, 'd', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
plt.text(0.525, 0.32, 'f', weight = 'bold', fontsize=8, transform=plt.gcf().transFigure)
file_out_name = file_path + '/../output/extended_data_figure1'
fig.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
fig.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)
fig.savefig(file_out_name+'.pdf', bbox_inches='tight', pad_inches = 0.05)