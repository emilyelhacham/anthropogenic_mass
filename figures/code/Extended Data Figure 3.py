# -*- coding: utf-8 -*-

import pandas as pd
import os

file_path = os.path.dirname(os.path.realpath(__file__))

# File uploads - Extended Data Figure 3
anthro_change = pd.read_excel(file_path + "/../../data/anthropogenic_mass_change.xlsx")

# Plotting
ax = anthro_change.plot(x='Year', y='% change ', legend=None, lw=2, xlim=(1900, 2020), ylim=(0, 6), xticks = [1900, 1920, 1940, 1960, 1980, 2000])
ax.set_ylabel('anthropogenic mass\nrelative annual change [%]', fontsize=7)
ax.set_xlabel('year', fontsize=7)
ax.set_xticklabels([1900, 1920, 1940, 1960, 1980, 2000], rotation=0, fontsize=6)
ax.set_yticklabels([0, 1, 2, 3, 4, 5,6], rotation=0, fontsize=6)
ax.text(1911.5, 0.35, 'WW1', size=6, color='k', alpha=0.5)
ax.text(1934.5, 2.55, 'great\ndepression', size=6, color='k', alpha=0.5, ha='center')
ax.text(1937, 1.1, 'WW2', size=6, color='k', alpha=0.5)
ax.text(1973, 5.82, '1973\noil crisis', size=6, color='k', alpha=0.5,ha='center')
ax.text(1979, 2.46, '1979\noil crisis', size=6, color='k', alpha=0.5,ha='center')
ax.hlines(y=0.65, xmin=1914,  xmax=1918, linestyle='-', linewidth=1.5, color='k', alpha=1)
ax.vlines(x=1914, ymin=0.62,  ymax=1.20, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.vlines(x=1918, ymin=0.62,  ymax=0.90, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.hlines(y=2.4, xmin=1929,  xmax=1939, linestyle='-', linewidth=1.5, color='k', alpha=1)
ax.vlines(x=1929, ymin=2.1,  ymax=2.42, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.vlines(x=1939, ymin=2.2,  ymax=2.42, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.hlines(y=1.4, xmin=1939,  xmax=1945, linestyle='-', linewidth=1.5, color='k', alpha=1)
ax.vlines(x=1939, ymin=1.37,  ymax=1.85, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.vlines(x=1945, ymin=1.37,  ymax=1.53, linestyle='-', linewidth=0.5, color='k', alpha=0.5)
ax.annotate('oil crisis1', xy=(1973, 5.3), xytext=(1964.5, 5.9), size=6, alpha=0, arrowprops=dict(arrowstyle="->", facecolor='black', lw=0.5))           
ax.annotate('', xy=(1979, 3.6), xytext=(1979, 3.05), size=6, alpha=0.5, ha='center', arrowprops=dict(arrowstyle="->", facecolor='black', lw=0.5))       
ax.annotate('dot-com\ncrash', xy=(2000, 3.4), xytext=(2000, 4.05), size=6, alpha=0.5, ha='center', arrowprops=dict(arrowstyle="->", facecolor='black', lw=0.5))           
ax.annotate('subprime\ncrisis', xy=(2007.5, 3.5), xytext=(2007.5, 2.3), size=6, alpha=0.5, ha='center',arrowprops=dict(arrowstyle="->", facecolor='black', lw=0.5))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.figure.set_figheight(2.3)
ax.figure.set_figwidth(3.5)
file_out_name = file_path + '/../output/extended_data_figure3'
ax.figure.savefig(file_out_name+'.png', bbox_inches='tight', pad_inches = 0.05, dpi = 600)
ax.figure.savefig(file_out_name+'.eps', bbox_inches='tight', pad_inches = 0.05)
ax.figure.savefig(file_out_name+'.svg', bbox_inches='tight', pad_inches = 0.05)