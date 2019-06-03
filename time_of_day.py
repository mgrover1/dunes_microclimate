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

def hot_cold_time(df):
    df['PartTime'] = " "
    count = 0
    for k in df['Hour']:
        if ((k>=12)):
            if ((k>=12) and (k<18)):
                df.at[count,['PartTime']] = "HotTime"
            else:
                df.at[count,['PartTime']] = 'Daytime'
        else:
            if (k>=6) and (k<12):
                df.at[count,['PartTime']] = "MorningTime"
            else:
                df.at[count,['PartTime']] = "ColdTime"
        count = count + 1
    return df
