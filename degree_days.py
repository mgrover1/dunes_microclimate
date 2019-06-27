#Import the neccessary libraries and functions

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import glob
from matplotlib import rcParams
from pandas import Series, DataFrame
import csv
import datetime as datetime
from datetime import datetime
import warnings
from tkinter import filedialog
from tkinter import *
warnings.filterwarnings('ignore')

def subset_datetime(df, start_time, end_time):
    """Subsets the dataframe for a given start time and end time

    Parameters
    ----------
    df : Pandas Dataframe
         Contains microclimate data or other types of data that need to be subset

    start_time : datetime object
         The beginning of the time interval

    end_time : datetime object
         The end of the time interval

    Returns
    -------
    Pandas Dataframe with the values between the time interval

    """
    import pandas as pd

    # Extract all dates after the start time
    df = df[df.datetime > start_time]

    # Extract all dates before the end time
    result_df = df[df.datetime < end_time]

    # Export the results
    return result_df

def plant_degree_day(dataframe):
    dataframe['Plant_Degree_Day'] = 0.0
    dataframe['Sum_Plant_Degree_Day'] = 0.0
    tCount = 0
    for year in dataframe.groupby('Year').sum().index:
        df = subset_datetime(dataframe, datetime(int(year), 1, 1), datetime(int(year)+1, 1, 1))
        yearly_plant_degree_day = []
        for i in df['temp']:
            if(i<= 32):
                dataframe.at[tCount,['Plant_Degree_Day']] = 0.0
                dataframe.at[tCount,['Sum_Plant_Degree_Day']] = sum(yearly_plant_degree_day)
            else:
                dataframe.at[tCount,['Plant_Degree_Day']]=np.round((i-32)/24,3)
                yearly_plant_degree_day.append(np.round((i-32)/24,3))
                dataframe.at[tCount,['Sum_Plant_Degree_Day']] = sum(yearly_plant_degree_day)
            tCount+=1
    return dataframe

def bug_degree_day(dataframe):
    dataframe['Bug_Degree_Day'] = 0.0
    dataframe['Sum_Bug_Degree_Day'] = 0.0
    bCount = 0
    for year in dataframe.groupby('Year').sum().index:
        df = subset_datetime(dataframe, datetime(int(year), 1, 1), datetime(int(year)+1, 1, 1))
        yearly_bug_degree_day = []
        for j in df['temp']:
            if(j<=50):
                dataframe.at[bCount,['Bug_Degree_Day']] = 0.0
                dataframe.at[bCount,['Sum_Bug_Degree_Day']] = sum(yearly_bug_degree_day)
            else:
                dataframe.at[bCount,['Bug_Degree_Day']] = np.round((j-50)/24,3)
                yearly_bug_degree_day.append((j-50)/24,3)
                dataframe.at[bCount,['Sum_Bug_Degree_Day']] = sum(yearly_bug_degree_day)
            bCount+=1
    return dataframe
