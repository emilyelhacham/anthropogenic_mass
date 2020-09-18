# -*- coding: utf-8 -*-

import pandas as pd
import os

file_path = os.path.dirname(os.path.realpath(__file__))

# File uploads - Extended Data Figure 4
metals = pd.read_excel(file_path + "/../../data/metals_category.xlsx")

# Plot colors  
c = ['#7a7f80', '#1c4966', '#cb6d51', '#f1d0a6']

# Plotting
ax = metals.plot(x='Year', kind='area', color = c, legend='reverse', xlim=(1900, 2014),ylim=(0, 33), xticks=[1910, 1930, 1950, 1970, 1990, 2010], yticks=[0, 5, 10, 15, 20, 25,30], lw=0)
ax.set_xticklabels([1910, 1930, 1950, 1970, 1990, 2010], rotation=0, fontsize=6)
ax.set_yticklabels([0, 5, 10, 15, 20, 25, 30], rotation=0, fontsize=6)
ax.set_xlabel('year', fontsize=7)
ax.set_ylabel('dry weight (Gigatonnes)', fontsize=7)
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), prop={'size': 6}, bbox_to_anchor=(0, 1.680/1.750), loc="upper left",frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.figure.set_figheight(2.3)
ax.figure.set_figwidth(3.5)
file_out_name = file_path + '/../output/extended_data_figure4'
ax.figure.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
ax.figure.savefig(file_out_name+'.eps', bbox_inches='tight', pad_inches = 0.05)
ax.figure.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)