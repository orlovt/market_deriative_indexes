import pandas as pd
import numpy as np 
import requests


from calendar import monthrange
import json
import math 


import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from helpers import helpers

class FFR_data(): 
    def get_futures(): 
        time = datetime.now()
        start_time = time - timedelta(90)
        ff = yf.download("ZQ=F", start=start_time, end=time) #start="2000-01-01", end="2022-11-09"
        ff.reset_index(inplace=True)
        ff = ff[['Date', 'Close']]
        ff.columns = ['Day', 'Price']

        ff['Day'] = ff['Day'].apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))

        priceoffutures_dict = {}
        for i in range(ff.shape[0]):
            priceoffutures_dict[ff['Day'][i]] = ff['Price'][i]
        return priceoffutures_dict

    #def assing_fpricesdf(df):
    #    df['PricePrevDay'] = df['PrevDay'].apply(lambda x : priceoffutures_dict[x] if x in priceoffutures_dict.keys() else 0)
    def assing_fpricesd(dt): 
        priceoffutures_dict = FFR_data.get_futures()
        if dt in priceoffutures_dict.keys():
            return priceoffutures_dict[dt]
        else: 
            return 0
    


    def get_prev_dates():
        url = 'https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[1] #current 

        #data prep and clean 
        df['dt'] = df['Date'].apply(lambda x:datetime.strptime(x, '%B %d, %Y'))
        df['dow'] = df['dt'].apply(lambda x : datetime.weekday(x))
        
        

        df = df[['Fed. Funds Rate', 'dt']]
        df.columns = ['R', 'D']

        return df

    def add_columns(df):
        df['DOW'] = df['D'].apply(lambda x : datetime.weekday(x))
        if 'R' in df.columns:
            df['R'] = df['R'].apply(helpers.split_rate)
        df['1DB'] = df.apply(lambda x: helpers.days_1_before(x['D'], x['DOW']), axis = 1)
        df['1WB'] = df.apply(lambda x: helpers.week_before(x['D'], x['DOW']), axis = 1)
        df['2WB'] = df.apply(lambda x: helpers.week_2_before(x['D'], x['DOW']), axis = 1)
        #df['3WB'] 
        df['1MB'] = df.apply(lambda x: helpers.month_before(x['D'], x['DOW']), axis = 1)
    def dates_list(day):
        day = datetime.strptime(day, "%Y-%m-%d")
        return {'1DB':helpers.days_1_before(day), '1WB':helpers.week_before(day), '2WB':helpers.week_2_before(day), '1MB':helpers.month_before(day)}


        return df

    def next_meeting(): #make automatic 
        date = '2022-12-14'
        d = {'D': ['2022-12-17'], 'R':['3.75%–4.00%']}
        df = pd.DataFrame(d)
        df['D'] = df['D'].apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))
        return df
        
        