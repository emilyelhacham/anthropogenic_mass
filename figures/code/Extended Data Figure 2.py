# -*- coding: utf-8 -*-

import pandas as pd
import os

file_path = os.path.dirname(os.path.realpath(__file__))

# File uploads - Extended Data Figure 2
anthro_comp = pd.read_excel(file_path +"/../../data/anthropogenic_mass_composition.xlsx")

# Plot colors
c = ['#352a86', '#0870de', '#93552F', '#333333', '#9b111e', '#fdc832', '#969696']

# Plotting
ax = anthro_comp.plot(x = 'year', kind= 'area', legend = 'reverse', xlim = (1900,2015), ylim = (0,1), xticks = [1910,1930,1950,1970,1990,2010], color = c, lw=0)
ax.set_ylabel('fraction',fontsize= 7)
ax.set_xlabel('year', fontsize= 7)
ax.set_xticklabels([1910,1930,1950,1970,1990,2010],rotation =0, fontsize= 6)
ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1],rotation =0, fontsize= 6)
ax.figure.set_figheight(2.3)
ax.figure.set_figwidth(3.5)
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles),reversed(labels),loc='center left', bbox_to_anchor=(1, 0.5),prop={'size': 6},frameon = True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
file_out_name = file_path + '/../output/extended_data_figure2'
ax.figure.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
ax.figure.savefig(file_out_name+'.eps', bbox_inches='tight', pad_inches = 0.05)
ax.figure.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)