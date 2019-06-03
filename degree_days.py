#Import the neccessary libraries and functions

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

def plant_degree_day(dataframe):
    dataframe['Plant_Degree_Day'] = 0.0
    dataframe['Sum_Plant_Degree_Day'] = 0.0
    tCount = 0
    for i in dataframe['temp']:
        if(i<= 32):
            dataframe.at[tCount,['Plant_Degree_Day']] = 0.0
        else:
            dataframe.at[tCount,['Plant_Degree_Day']]=np.round((i-32)/24,3)
        dataframe['Sum_Plant_Degree_Day'][i] = sum(dataframe.Plant_Degree_Day[0:sum(i+1)])
        tCount = tCount+1


    return dataframe

def bug_degree_day(dataframe):
    dataframe['Bug_Degree_Day']
    dataframe['Sum_Bug_Degree_Day']
    bCount = 0
    for j in dataframe['temp']:
        if(j<=50):
            dataframe.at[bCount,['Bug_Degree_Day']] = 0.0
        else:
            dataframe.at[bCount,['Bug_Degree_Day']] = np.round((j-50)/24,3)
        dataframe['Sum_Bug_Degree_Day'][i] = sum(dataframe.Bug_Degree_Day[0:sum(i+1)])
        bCount = bCount+1
    return dataframe 
