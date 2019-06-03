#Import the neccessary libraries and functions
#This script was derived from a presentation at the AMS Annual Meeting in Austin, TX

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import glob
from matplotlib import rcParams
from pandas import Series, DataFrame
import seaborn as sb
import csv
import datetime as datetime
from datetime import datetime
import warnings
from tkinter import filedialog
from tkinter import *
warnings.filterwarnings('ignore')

def _passed(date_str, series):
    return series[date_str]

#########################################################
# PERSISTENCE TEST
#########################################################
#Checks to see if there are repeat values in the data
import argparse
import sys

def _passed(date_str, series):
    return series[date_str]

def persist_test(value, max_diff, min_stddev):
    #Create a dataframe to store the values
    columns = ['date','value','max_diff','max_diff_result',
              'min_stddev', 'min_stddev_result', 'result']
    df = pd.DataFrame(index=value.index, columns = columns)

    #Creates a column to detail the date
    df['date'] = [(str(t.year)+ '-' + str(t.month) +'-' + str(t.day)) \
                 for t in df.index]
    df['value'] = value
    df['max_diff'] = max_diff
    df['min_stddev'] = min_stddev

    max_diff_f = lambda x: np.less_equal((x.max() - x.min()), max_diff)
    min_stddev_f = lambda x: np.greater_equal(x.std(), min_stddev)
    final_f = lambda x: np.logical_and(max_diff_f(x), min_stddev_f(x))

    grouped = df.groupby('date')
    md = grouped['value'].apply(max_diff_f)
    ms = grouped['value'].apply(min_stddev_f)
    pt = grouped['value'].apply(final_f)

    df['max_diff_result'] = True
    df['max_diff_result'] = df.apply(lambda row: _passed(row['date'], md), axis = 1)

    df['min_stddev_result'] = True
    df['min_stddev_result'] = df.apply(lambda row: _passed(row['date'], ms), axis = 1)

    df['result'] = df.apply(lambda row: _passed(row['date'], pt), axis =1)

    #except Exception as e:
        #sys.stderr.write(str(e) + '\n')
        #df = False
    df['result'] = True
    return df

#########################################################
# RANGE TEST
#########################################################
#Tests to see if values are within certain thresholds
def _pdtest(value, max_value, min_value):
    try:
        df = pd.DataFrame(index = value.index, columns = ['value', 'max_value', 'min_value', 'result'])
        df['value'] = value
        df['max_value'] = max_value
        df['min_value'] = min_value

        l = np.less_equal(value, max_value)
        g = np.greater_equal(value, min_value)

        df['result'] = np.logical_and(l,g)

    except Exception as e:

        sys.stderr.write(str(e) + '\n')
        df = False

    return df

def test(value, max_value, min_value):

#    return False

    #Lambda function checks to see if 'test' function parameters are floats or ints
    _iif = lambda x: isinstance(x, (int,float))

    try:
        if isinstance(value, pd.Series):
            result = _pdtest(value, max_value, min_value)

        elif (_iif(value)) and (_iif(max_value)) and (_iif(min_value)):
            if value >= min_value and value <= max_value:
                result = True

    except Exception  as e:
        sys.stderr.write(str(e) + '\n')

    return result


def range_test(value, max_value, min_value):
    #Runs through the function
    return(test(value, max_value, min_value))




def step_test(value, max_diff, num_steps = 1):
    try:

        columns = ['value', 'prev_value', 'max_diff', 'num_steps', 'result']
        df = pd.DataFrame(index = value.index, columns = columns)
        prev_value = value[1:]
        df['value'] = value[:-1]
        df['prev_value'] = prev_value
        df['max_diff'] = max_diff
        df['num_steps'] = num_steps

        value = value[:-1]
        d = value - prev_value
        a = np.fabs(d)

        df['result'] = np.less_equal(a, max_diff)

    except:
        df = False

    return df
