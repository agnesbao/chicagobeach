# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:17:00 2017

@author: Xiaojun

This script grab the most recent 1000 data from water and weather sensor, and 
plot today's water quality (turbidity) hour by hour, and the past month's water
quality day by day.
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt


water_url = "https://data.cityofchicago.org/resource/46rk-hgnz.json"
weather_url = "https://data.cityofchicago.org/resource/77jv-5zb8.json"

def request_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    return pd.DataFrame(data)

def plot_water_quality_today(df):
    timestamp = pd.to_datetime(df.measurement_timestamp)
    quality = df.turbidity[timestamp.dt.date==pd.to_datetime('today').date()]
    quality.index = timestamp[timestamp.dt.date==pd.to_datetime('today').date()].dt.time
    plt.plot(quality,'.-')
    plt.xticks(quality.index,rotation=90)
    plt.ylabel(quality.name)
    plt.title(pd.to_datetime('today').date())
    plt.show()
    
def plot_water_quality_past_month(df):
    timestamp = pd.to_datetime(df.measurement_timestamp)
    quality = df.turbidity[timestamp.dt.date>pd.to_datetime('today').date()-pd.Timedelta('30 days')]
    quality = quality.astype(float)
    quality.index = timestamp[timestamp.dt.date>pd.to_datetime('today').date()-pd.Timedelta('30 days')]
    plt.plot(quality.groupby(quality.index.date).mean(),'.-')
    plt.xticks(rotation=90)
    plt.ylabel(quality.name)
    plt.show()

water_df = request_data(water_url)
weather_df = request_data(weather_url)

plot_water_quality_today(water_df)
plot_water_quality_past_month(water_df)

