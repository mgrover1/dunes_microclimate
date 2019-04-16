def data_read_in(file_list):
    result = file_list
    appended_data=[]
    pd.DataFrame()
    for i in result:
        try:
            #Splits the file name so the sensor name and type can be seperated
            sensor,type = i.split('_')

            #Subsets the important info from the name
            type = type[7:]
            type = type[:-4]

            #Reads in the data and assigns it to a dataframe using Pandas
            df = pd.read_csv(i,header=1,usecols=[1,2,3],names=['datetime','temp','light_intensity'])

            #Create new columns that can be referenced to later
            df['source']=i
            df['site']= sensor
            df['type']=type

            #Create a list of all the dataframe names to be referenced when assembling master dataframe
            appended_data.append(df)

            #Removes possible errors from occuring
        except:AttributeError

    #Assemble all dataframes into one master file
    df = pd.concat(appended_data)

    #Export all the observations to a csv
    df.to_csv('full_dataframe.csv')

    #Assemble the dataframe and seperate datetime features so they can be used later
    x = pd.DataFrame(df)
    x['datetime'] = pd.to_datetime(x['datetime'])
    x['temp'] = pd.to_numeric(x['temp'])
    x['light_intensity'] = pd.to_numeric(x['light_intensity'])
    x['Year'] = pd.DatetimeIndex(x['datetime']).year
    x['Month'] = pd.DatetimeIndex(x['datetime']).month
    x['Day'] = pd.DatetimeIndex(x['datetime']).day
    x['Week'] = pd.DatetimeIndex(x['datetime']).week
    x['Time'] = pd.DatetimeIndex(x['datetime']).time
    x['Hour'] = pd.DatetimeIndex(x['datetime']).hour
    x['Minute'] = pd.DatetimeIndex(x['datetime']).minute

    return x
