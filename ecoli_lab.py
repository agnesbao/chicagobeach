# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 13:15:03 2017

@author: Xiaojun
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def fix_date(date_str):
    if type(date_str)==str:
        return date_str.replace('0016','2016')

def select_data(datadf, measure, year, beach):
    if measure=="culture":
        data_year = datadf[pd.to_datetime(datadf['Culture Sample 1 Timestamp']).dt.year==year]
        data_beach = data_year[['Culture Reading Mean', 'Culture Sample 1 Timestamp']][data_year.Beach==beach]
        data_beach = data_beach.rename(columns={'Culture Reading Mean':'reading','Culture Sample 1 Timestamp':'sampletime'})
        threshold = 235 # unsafe for swimming
    elif measure=="dna":
        data_year = datadf[pd.to_datetime(datadf['DNA Sample Timestamp']).dt.year==year]
        data_beach = data_year[['DNA Reading Mean', 'DNA Sample Timestamp']][data_year.Beach==beach]
        data_beach = data_beach.rename(columns={'DNA Reading Mean':'reading','DNA Sample Timestamp':'sampletime'})
        threshold = 1000
    data_beach.sampletime = pd.to_datetime(data_beach.sampletime).dt.date
    data_beach = data_beach.sort_values(by='sampletime')
    return data_beach

def barplot_annual(datadf, measure, year):
    # plot annual mean of ecoli level at each beach
    # datadf: culture or dna
    # measure: "culture" or "dna"
    if measure=="culture":
        data_year = datadf['Culture Reading Mean'][pd.to_datetime(datadf['Culture Sample 1 Timestamp']).dt.year==year].groupby(datadf.Beach)
        threshold = 235 # unsafe for swimming
    elif measure=="dna":
        data_year = datadf['DNA Reading Mean'][pd.to_datetime(datadf['DNA Sample Timestamp']).dt.year==year].groupby(datadf.Beach)     
        threshold = 1000
    data_mean = data_year.mean().sort_values()
#    data_count = data_year.count()
#    print(data_count)
    plt.bar(range(len(data_mean)),data_mean.values)
    plt.plot([0, len(data_mean)],[threshold, threshold],'r--')
    plt.xticks(range(len(data_mean)),data_mean.index,rotation=90)
    plt.ylabel(data_mean.name)
    plt.title(str(year)+' Chicago Beach E.coli '+measure.upper()+' Test')
    plt.show()
    
lab_df = pd.read_csv('Beach_Lab_Data.csv')

# fix timestamp
lab_df['Culture Sample 1 Timestamp'] = lab_df['Culture Sample 1 Timestamp'].apply(fix_date)
lab_df['Culture Sample 2 Timestamp'] = lab_df['Culture Sample 2 Timestamp'].apply(fix_date)

# drop lab data with no beach information
lab_df = lab_df.dropna(subset=['Beach'])
# select e.coli culture data and dna data
culture = lab_df.dropna(subset=['Culture Reading Mean'])
dna = lab_df.dropna(subset=['DNA Reading Mean'])

# plot E.coli test annual data
barplot_annual(dna,'dna',2017)

# plot dna and culture of Montrose beach in 2016
data_beach = select_data(dna,'dna',2016,'North Avenue')
plt.plot(data_beach.sampletime, data_beach.reading, label = 'DNA')
data_beach = select_data(culture,'culture',2016,'North Avenue')
plt.plot(data_beach.sampletime, data_beach.reading, 'r', label = 'Culture')
plt.xticks(rotation=90)
plt.title('North Avenue Beach 2016')
plt.legend()
plt.show()