import pandas as pd

def subset_site_type(df, site_name, site_type):
    ''' Input the output from the subset_max_min to be subset for each site and site type
    df = original dataframe
    site_name = name of the site as a string (ex. 'LP1' )
    site_type = type of site as a string (ex. 'ground')

    output: a subset dataframe
    '''
    df1 = df[df.site == site_name]
    df2 = df1[df1.type == site_type]

    return df2

def subset_variables(df, site_name, site_type, sum_type):
    '''Assembles the maximum and minimum dataframes into a single dataframe
    '''

    #Subsets the neccessary site name and type from the whole dataframe
    subset_df = subset_site_type(df, site_name, site_type)

    #Find maximums, minimums, and means
    max_df = subset_df[['site','type','temp','light_intensity']].resample(sum_type).max()
    min_df = subset_df[['site','type','temp','light_intensity']].resample(sum_type).min()
    mean_df = subset_df[['site','type','temp','light_intensity']].resample(sum_type).mean()

    #Ensure the temperatures are numeric so DTR can be calculated
    max_df['temp'] = pd.to_numeric(max_df.temp)
    min_df['temp'] = pd.to_numeric(min_df.temp)

    #Calculate DTR (Diurnal Temperature Range)
    dtr_df = max_df.temp - min_df.temp

    #Setup the dataframe
    df = pd.DataFrame({'site':max_df.site,
                       'type':max_df.type,
                       'maximum_temperature':max_df.temp,
                       'minimum_temperature':min_df.temp,
                       'mean_temp':mean_df.temp,
                       'DTR':dtr_df,
                      'maximum_light':max_df.light_intensity,
                      'minimum_light':min_df.light_intensity,
                      'mean_light':mean_df.light_intensity})

    return df
