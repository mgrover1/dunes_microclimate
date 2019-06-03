#Import the neccessary libraries and functions
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
import numpy as np
import re
import os
import interactive_file_selection
import glob
from matplotlib import rcParams
from pandas import Series, DataFrame
import seaborn as sb
import csv
import datetime as datetime
from datetime import datetime
import warnings
import tkinter as tk
from tkinter import filedialog
from tkinter import *
warnings.filterwarnings('ignore')

from subset import subset_variables, subset_site_type

def multi_panel_plot(df, plot_vars, frequency):
    '''Creates a multiple panel plot using an input dataframe, and subsets based on
    the number of sensor sites and types. The user also as the option to save the figure

    df = the input dataframe
    plot_vars = desired variables as a string (ex. max_min_temperature, max_min_light,
    diurnal_temperature range)
    frequency = the type of summary requested (ex. daily, weekly, monthly, yearly)
    savefig = True or False, depending on whether you would like to save the figure
    '''
    from subset import subset_variables, subset_site_type
    plot_variables = plot_vars

    #Make calling the degree sign easier
    degree_sign= u'\N{DEGREE SIGN}'

    #Setup a dictionary to call different colors based on the variable type
    colors = {'maximum_temperature':'tab:red',
              'minimum_temperature':'tab:blue',
              'maximum_light':'tab:red',
              'minimum_light':'tab:blue',
              'DTR':'black'}

    #Add units for the different graphs that are created
    units = {'maximum_temperature':f'{degree_sign}F',
             'minimum_temperature':f'{degree_sign}F',
             'maximum_light':'lumens/ft2',
             'minimum_light':u'lumens/ft2',
             'DTR':f'{degree_sign}F'}

    #Make calling different summary types easier
    freq = {'yearly':'Y',
            'Yearly':'Y',
            'monthly':'M',
            'Monthly':'M',
            'weekly':'W',
            'Weekly':'W',
            'daily':'D',
            'Daily':'D'}

    summary_variables = {'max_min_temperature':['maximum_temperature','minimum_temperature'],
                        'max_min_light':['maximum_light','minimum_light'],
                        'diurnal_temperature_range':['DTR']}

    def format_varname(varname):
        if varname == 'DTR':
            title = 'Diurnal Temperature Range'
            label = 'DTR'
        else:
            parts = varname.split('_')
            title = parts[1].title()
            label = varname.replace('_',' ').title()
        return title, label

    #Determine what the summary variables are
    plot_variables = summary_variables[plot_variables]
    summary_typ = freq[frequency]

    #Prepare to plot
    site_names = list(df.groupby('site').count().index.values)
    site_types = list(df.groupby('type').count().index.values)

    #Create a loop that will create a plot
    for site in site_names:

        #Setup the figure and axes
        fig, axes = plt.subplots(1, len(site_types), sharex =True,sharey= True, figsize = (5*len(site_types),5))


        for ax, site_type in zip(axes, site_types):
            df1 = subset_variables(df, site, site_type, summary_typ)
            for var_name in plot_variables:
                title, label = format_varname(var_name)
                color = colors[var_name]
                ax.plot(df1.index, df1[var_name], color=color, label=label)
                ax.legend()
                ax.set_ylabel(title)
                ax.set_title(f'Site {site} {site_type}')
                ax.set_xlabel('Time')
                ax.xaxis.set_major_formatter(DateFormatter('%m/%Y'))
                ax.xaxis.set_major_locator(YearLocator())
                ax.legend()
        plt.savefig(f'{site}_multipanel.png', dpi=300)
