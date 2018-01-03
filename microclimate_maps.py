###############################################################
# Program Name: microclimate_plots.py
#
# Purpose: Import data from microclimate stations at the Indiana
# Dunes National Lake Shore, and sensor data from the Weather
# Underground API from Beverly Shores, IN, just East of the Dunes. 
#
# Graph the temperature and light values for the various sensors
# grouped by both the sensor type and sensor site
#
# Calculate the Diurnal Temperature Range (Maximum Temperature-
# Minimum Temperature), and Daily Cooling Ratio (Temperature at the 
# Microclimate Sensor / Temperature at the Beverly Shores Station)
#
# Input: .csv files containing light and temperature data for 
#         individual sensors (ex. LP7_ground_2012_2013.csv)
#
# Output: Four Panel Plots seperated by Sensor Type and Sensor Location
#         
#        
# Honor Code: "I have neither given or received, nor have I tolerated
# others' use of unauthorized aid."      -Maxwell A. Grover
#
################################################################


#Import the neccessary libraries 
import pandas as pd
import bokeh as bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_file, show, export_png
import numpy as np
import datetime as datetime,time
from datetime import datetime
import csv
import urllib as urllib
import json

#Definitions to be used throughout the script 

def name_extractor(filename):
    '''
    Determines the sensor name and sensor type and assigns the file a sensor title
    
    Original file format example: LP7_pole_2012_2013.csv
    
    Converted File Name: LP7 Pole Sensor
    
    Input: Filename (string)
    
    Output: Sensor Title (string), Sensor Type (string), Sensor Name (string)
    '''
    #Take off the ending of the file path
    filename = filename[:-14]

    #Determine the type of sensor 
    if 'ground' in filename:
        sensor_type='Ground'
        sensor_name=filename[:-7]
    elif 'pole' in filename:
        sensor_type = 'Pole'
        sensor_name=filename[:-5]
    else:
        sensor_type = 'Tube'
        sensor_name =filename[:-5]
        
    #Assemble the title
    sensor_title = sensor_name+' '+sensor_type+' Sensor'
    
    #Returns the title
    return sensor_title,sensor_type,sensor_name


def wx_underground_pws_may2012(station_id):
    '''
    Brings in May 2012 Personal Weather Station information from the station of choice.
    It utilizes Weather Underground's API, which provided a help page that allowed me to 
    access the data.
    
    input: Station identifier found on weather underground for a personal weather station (string)
    
    output: Pandas dataframe containing maximum temperature, minimum temperature, and diurnal 
    temperature range values for each day in the month of May 2012 in the format of station_df 
    '''
    #Import the needed libraries
    import urllib
    import json
    import datetime as datetime
    from datetime import datetime
    
    #Create lists to append later in the script to be written to a dataframe

    #Maximum temperature
    maxtemp = []
    #Minimum temperature
    mintemp = []
    #Timestamp (Datetime format)
    timestamp = []
    #Diurnal Temperature Range (Maximum-Minimum Temperature)
    dtr = []
    #Create a list of days for the month of May 
    day_list = []

    for i in range(31):
        i+=1
        #Make sure it is in the correct format to be read in using the weather underground api
        i = str('%02d'%i)
        day_list.append(i)

    #Read in the data from the weather underground API to be used to compare the station data
    for i in range(len(day_list)):
    
        #Access the Personal Weather Station information from the Weather Underground API
        f = urllib.request.urlopen('http://api.wunderground.com/api/fad377a2fb7f6004/geolookup/history_201205'+day_list[i]+'/q/pws:'+station_id+'.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
    
        #Subset the variables from the parsed json data
        location = parsed_json['location']['city']
        date = parsed_json['history']['dailysummary'][0]['date']
        day = int(date['mday'])
        month = int(date['mon'])
        year = int(date['year'])
    
        #From the daily summary information, extract the maximum and minimum temperatures for each day
        max_temp = parsed_json['history']['dailysummary'][0]['maxtempi']
        max_temp = float(max_temp)
        min_temp = parsed_json['history']['dailysummary'][0]['mintempi']
        min_temp = float(min_temp)
        DTR = max_temp - min_temp
    
    #Add to the lists for the timestamp, maximum, and minimums for the station
        timestamp.append(datetime(year,month,day))
        maxtemp.append(max_temp)
        mintemp.append(min_temp)
        dtr.append(DTR)

    #Format the data into numpy arrays to be read into a single Pandas Array
    timestamp = np.array(timestamp)
    maxtemp = np.array(maxtemp)
    mintemp = np.array(mintemp)
    dtr = np.array(dtr)

    
    #Create a pandas array containing the May 2012 data from the Beverly Shores Weather Underground Station
    station_df = pd.DataFrame({'timestamp':timestamp,'maxtemp':maxtemp,'mintemp':mintemp,'DTR':dtr})
    station_df = station_df.set_index('timestamp')
    
    return(station_df)


def maydata(file_name,bev_shores_df):
    """
    Takes in a csv file containing microclimate data with the proper formatting then compares it to the 
    nearby Beverly Shores observation station taken from the Weather Underground API. It produces a 
    pandas dataframe that can then be used to create various maps or other analysis. This only subsets
    the month of May 2012. 
	 
    Input: Name of the file (ex. LP7_tube_2012_2013.csv)
    Beverly Shores Dataframe (output from the wxunderground defintion 
               
    Output: Pandas Dataframe with the daily maximum temperature, daily minimum temperature, daily maximum
    light intensity, the morning temperature (AM-12PM), afternoon temperature (12PM-6PM), diurnal 
    temperature range (temprange), and daily cooling ratio (dcr). 
    """
    
    #Bring in the sensor data from the Indiana Dunes 
    test_df = pd.read_csv(file_name)
    
    #Convert the timestamp column to timestamp objects
    test_df.timestamp = pd.to_datetime(test_df.timestamp)
    sens_df = test_df.set_index("timestamp")

    #Subset May temperatures from the Dunes sensor dataset 
    may_sens_df = sens_df[datetime(2012,5,1):datetime(2012,5,31,23)]

    #Convert both the temperature and light values to numeric values 
    may_sens_df.temp = pd.to_numeric(may_sens_df.temp)
    may_sens_df.light = pd.to_numeric(may_sens_df.light)

    #Find the maximum and minimum temperatures for each day
    daily_max_temps = pd.DataFrame(may_sens_df.temp.resample('D').max())
    daily_min_temps = pd.DataFrame(may_sens_df.temp.resample('D').min())

    #Find the range in temperatures for each day 
    temp_range = daily_max_temps.temp - daily_min_temps.temp

    #Subset the hourly temperatures in 6 hour intervals 
    hourly6_avg_temps = pd.DataFrame(may_sens_df.temp.resample('6H').mean())

    #Calculate the average morning and average evening temperatures 
    morning_06_12 = pd.DataFrame(hourly6_avg_temps[hourly6_avg_temps.index.hour == 6]).resample('D').mean()
    afternoon_12_18 = pd.DataFrame(hourly6_avg_temps[hourly6_avg_temps.index.hour == 12]).resample('D').mean()
    
    #Calculate the daily cooling ratio, using the microclimate station as the observation, and Beverly Shores as the reference
    #This is taken from a paper found using this website link
    dcr = temp_range/bev_shores_df['DTR']
    
    #Daily Max Light Values 
    daily_max_light = pd.DataFrame(may_sens_df.light.resample('D').max())
    frames = [daily_max_temps, daily_min_temps, daily_max_light, morning_06_12, afternoon_12_18,temp_range,dcr]
    results_df = pd.concat(frames, keys = ['maxtemp', 'mintemp','maxlight','morningtemp','afternoontemp','temprange','dcr'],axis = 1)
    
    return(results_df)


def single_sensor_fourpanel(df1_file,df2_file,df3_file,height,width):
    '''
    Assembles a four panel plot including the maximum temperature for each sensor on a line graph, the minimum 
    temperature for each sensor on a line graph, the daily cooling ratio for each sensor on a line graph, 
    and the light value for each sensor. This is meant for the same sensor stie, but different sensor types.
    
    input: Dataframe from the maydata output (1)
           Dataframe from the maydata output (2)
           Dataframe from the maydata output (3)
           Dataframe's original file (1)
           Dataframe's original file (2)
           Dataframe's original file (3)
           Height of the chart (integer)
           Width of the chart (integer)
           
    output: Four panel plot saved as the sensor name and type saved as an html file
    '''
    
    from bokeh.io import output_file, show
    from bokeh.layouts import gridplot
    from bokeh.palettes import Viridis3
    from bokeh.plotting import figure
    
    width = int(width)
    height = int(height)
    
    #Create dataframes for the various sensors 
    
    df1 = maydata(df1_file,bev_shores_df)
    df2 = maydata(df2_file,bev_shores_df)
    df3 = maydata(df3_file,bev_shores_df)
    
    #Find Name/Title and Type for Sensor 1 (They are all the same type)
    sensor1_title = name_extractor(df1_file)[0]
    sensor1_type = name_extractor(df1_file)[1]
    sensor1_name = name_extractor(df1_file)[2]
    
    #Find Name/Title for Sensor 2
    sensor2_title = name_extractor(df2_file)[0]
    sensor2_type = name_extractor(df2_file)[1]
    sensor2_name = name_extractor(df2_file)[2]
    
    #Find Name/Title for Sensor 3
    sensor3_title = name_extractor(df3_file)[0]
    sensor3_type = name_extractor(df3_file)[1]
    sensor3_name = name_extractor(df3_file)[2]
    
    #Define the output file 
    output_file(sensor1_name+'_'+'_four_panel'+'.html')

    #Make the plots
    #Maximum/Afternoon Temperatures 
    p = figure(title="Maximum Temperature May 2012 "+sensor1_name,plot_width=width,plot_height=height,x_axis_type = 'datetime')
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Temperature (F)"
    p.line(x=df1.index,y=df1['maxtemp']['temp'],color='red',legend = sensor1_type+' Microclimate Sensor')
    p.line(x=df2.index,y=df2['maxtemp']['temp'],color='green',legend = sensor2_type+' Microclimate Sensor')
    p.line(x=df3.index,y=df3['maxtemp']['temp'],color='blue',legend = sensor3_type+' Microclimate Sensor')
     
    #Line graph for max and min temperatures
    p2 = figure(title="Minimum Temperature May 2012 "+sensor1_name,plot_width=width,plot_height=height,x_axis_type = 'datetime')
    p2.xaxis.axis_label = "Date"
    p2.yaxis.axis_label = "Temperature (F)"
    p2.line(x=df1.index,y=df1['mintemp']['temp'],color='red',legend = sensor1_type+' Microclimate Sensor')
    p2.line(x=df2.index,y=df2['mintemp']['temp'],color='green',legend = sensor2_type+' Microclimate Sensor')
    p2.line(x=df3.index,y=df3['mintemp']['temp'],color='blue',legend = sensor3_type+' Microclimate Sensor')

    #Line graph for Daily Cooling Ratio
    p3 = figure(title="Daily Cooling Ratio May 2012 "+sensor1_name,plot_width=width,plot_height=height,x_axis_type='datetime')
    p3.xaxis.axis_label = "Date"
    p3.yaxis.axis_label = "Unitless (F/F)"
    p3.line(x=df1.index,y=df1['dcr'][0],color='red',legend = sensor1_type+' Microclimate Sensor')
    p3.line(x=df2.index,y=df2['dcr'][0],color='green',legend = sensor2_type+' Microclimate Sensor')
    p3.line(x=df3.index,y=df3['dcr'][0],color='blue',legend = sensor3_type+' Microclimate Sensor')

    #Line graph for Maximum Light value for each day
    p4 = figure(title="Daily Maximum Light Intensity May 2012 "+sensor1_name,plot_width=width,plot_height=height,x_axis_type='datetime')
    p4.xaxis.axis_label = "Date"
    p4.yaxis.axis_label = "Light Value (Lum/ft^2)"
    p4.line(x=df1.index,y=df1['maxlight']['light'],color='red',legend=sensor1_type+' Microclimate Sensor')
    p4.line(x=df2.index,y=df2['maxlight']['light'],color='green',legend=sensor2_type+' Microclimate Sensor')
    p4.line(x=df3.index,y=df3['maxlight']['light'],color='blue',legend=sensor3_type+' Microclimate Sensor')
    
    grid = gridplot([[p,p2],[p3,p4]])
    show(grid)
    
    
def multiple_sensor_fourpanel(df1_file,df2_file,df3_file,height,width):
    '''
    Assembles a four panel plot including the maximum temperature for each sensor on a line graph, the minimum 
    temperature for each sensor on a line graph, the daily cooling ratio for each sensor on a line graph, 
    and the light value for each sensor. This is meant for the same sensor type, but different sensor sites.
    
    input: Dataframe from the maydata output (1)
           Dataframe from the maydata output (2)
           Dataframe from the maydata output (3)
           Dataframe's original file (1)
           Dataframe's original file (2)
           Dataframe's original file (3)
           Height of the chart (integer)
           Width of the chart (integer)
           
    output: Four panel plot saved as the sensor name and type saved as an html file
    '''
    
    from bokeh.io import output_file, show
    from bokeh.layouts import gridplot
    from bokeh.palettes import Viridis3
    from bokeh.plotting import figure
    
    width = int(width)
    height = int(height)
    
    #Create dataframes for the various sensors 
    
    df1 = maydata(df1_file,bev_shores_df)
    df2 = maydata(df2_file,bev_shores_df)
    df3 = maydata(df3_file,bev_shores_df)
    
    #Find Name/Title and Type for Sensor 1 (They are all the same type)
    sensor1_title = name_extractor(df1_file)[0]
    sensor1_type = name_extractor(df1_file)[1]
    sensor1_name = name_extractor(df1_file)[2]
    
    #Find Name/Title for Sensor 2
    sensor2_title = name_extractor(df2_file)[0]
    sensor2_name = name_extractor(df2_file)[2]
    
    #Find Name/Title for Sensor 3
    sensor3_title = name_extractor(df3_file)[0]
    sensor3_name = name_extractor(df3_file)[2]
    
    #Define the output file 
    output_file(sensor1_type+'_'+'_four_panel'+'.html')

    #Make the plots
    
    #Maximum/Afternoon Temperatures 
    p = figure(title="Maximum Temperature May 2012 "+sensor1_type,plot_width=width,plot_height=height,x_axis_type = 'datetime')
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Temperature (F)"
    p.line(x=df1.index,y=df1['maxtemp']['temp'],color='red',legend = sensor1_name+' Microclimate Sensor')
    p.line(x=df2.index,y=df2['maxtemp']['temp'],color='green',legend = sensor2_name+' Microclimate Sensor')
    p.line(x=df3.index,y=df3['maxtemp']['temp'],color='blue',legend = sensor3_name+' Microclimate Sensor')
     
    #Line graph for max and min temperatures
    p2 = figure(title="Minimum Temperature May 2012 "+sensor1_type,plot_width=width,plot_height=height,x_axis_type = 'datetime')
    p2.xaxis.axis_label = "Date"
    p2.yaxis.axis_label = "Temperature (F)"
    p2.line(x=df1.index,y=df1['mintemp']['temp'],color='red',legend = sensor1_name+' Microclimate Sensor')
    p2.line(x=df2.index,y=df2['mintemp']['temp'],color='green',legend = sensor2_name+' Microclimate Sensor')
    p2.line(x=df3.index,y=df3['mintemp']['temp'],color='blue',legend = sensor3_name+' Microclimate Sensor')

    #Line graph for Daily Cooling Ratio
    p3 = figure(title="Daily Cooling Ratio May 2012 "+sensor1_type,plot_width=width,plot_height=height,x_axis_type='datetime')
    p3.xaxis.axis_label = "Date"
    p3.yaxis.axis_label = "Unitless (F/F)"
    p3.line(x=df1.index,y=df1['dcr'][0],color='red',legend = sensor1_name+' Microclimate Sensor')
    p3.line(x=df2.index,y=df2['dcr'][0],color='green',legend = sensor2_name+' Microclimate Sensor')
    p3.line(x=df3.index,y=df3['dcr'][0],color='blue',legend = sensor3_name+' Microclimate Sensor')

    #Line graph for Maximum Light value for each day
    p4 = figure(title="Daily Maximum Light Intensity May 2012 "+sensor1_type,plot_width=width,plot_height=height,x_axis_type='datetime')
    p4.xaxis.axis_label = "Date"
    p4.yaxis.axis_label = "Light Value (Lum/ft^2)"
    p4.line(x=df1.index,y=df1['maxlight']['light'],color='red',legend=sensor1_name+' Microclimate Sensor')
    p4.line(x=df2.index,y=df2['maxlight']['light'],color='green',legend=sensor2_name+' Microclimate Sensor')
    p4.line(x=df3.index,y=df3['maxlight']['light'],color='blue',legend=sensor3_name+' Microclimate Sensor')
    
    grid = gridplot([[p,p2],[p3,p4]])
    show(grid)

#Pull the data for the Beverly Shores Weather Underground Station
bev_shores_df = wx_underground_pws_may2012('KINBEVER2')

#Create plots for each one of the sensor types at different stations
multiple_sensor_fourpanel('LP7_tube_2012_2013.csv','LP17_tube_2012_2013.csv','T197_tube_2012_2013.csv',600,800)
multiple_sensor_fourpanel('LP7_ground_2012_2013.csv','LP17_ground_2012_2013.csv','T197_ground_2012_2013.csv',600,800)
multiple_sensor_fourpanel('LP7_pole_2012_2013.csv','LP17_pole_2012_2013.csv','T197_pole_2012_2013.csv',600,800)

#Create plots for each one of the individual stations
single_sensor_fourpanel('LP7_ground_2012_2013.csv','LP7_pole_2012_2013.csv','LP7_tube_2012_2013.csv',600,800)
single_sensor_fourpanel('LP17_ground_2012_2013.csv','LP17_pole_2012_2013.csv','LP17_tube_2012_2013.csv',600,800)
single_sensor_fourpanel('T197_ground_2012_2013.csv','T197_pole_2012_2013.csv','T197_tube_2012_2013.csv',600,800)
