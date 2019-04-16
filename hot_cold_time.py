def hot_cold_time(df):
    df['PartTime'] = " "
    count = 0
    for k in df['Hour']:
        if ((k>=12)):
            if ((k>=12)) and (k<18)):
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
