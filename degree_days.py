def plant_degree_day(dataframe):
    dataframe['Plant_Degree_Day'] = 0.0
    tCount = 0
    for i in dataframe['temp']:
        if(i<= 32):
            dataframe.at[tCount,['Plant_Degree_Day']] = 0.0
        else:
            x.at[tCount,['Plant_Degree_Day']]=np.round((i-32)/24,3)
        tCount = tCount+1
    return dataframe

def bug_degree_day(dataframe):
    dataframe['Bug_Degree_Day']
    bCount = 0
    for j in dataframe['temp']:
        if(j<=50):
            dataframe.at[bCount,['Bug_Degree_Day']] = 0.0
        else:
            dataframe.at[bCount,['Bug_Degree_Day']] = np.round((j-50)/24,3)
    bCount = bCount+1
    
