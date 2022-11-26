import pandas as pd
import numpy as np 
import requests


from calendar import monthrange
import json
import math 


import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class helpers():
        def split_rate(s):
            if chr(8211) in s:
                wow = s.split(chr(8211))
                s1 = wow[0][:-1]
                s2 = wow[1][:-1]
                return (float(s1) + float(s2)) / 2
            else:
                return float(s[:-1]) 

        #adding day before and day after 
        def N_filter(dt, dow):
            
                if dow >= 4: 
                    return dt + timedelta(days=(7-dow))
                else: 
                    return dt + timedelta(days=1)

        def B_filter(dt, dow):
            
                if dow == 6: 
                    return dt - timedelta(days=(2))
                elif dow == 0:
                    return dt - timedelta(days=3) 
                else: 
                    return dt - timedelta(days=1)

class FFR_probs():
    def test():
        return 0

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


    def get_dates():
        url = 'https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[1].iloc[:1] #current 

        #data prep and clean 
        df['dt'] = df['Date'].apply(lambda x:datetime.strptime(x, '%B %d, %Y'))
        df['dow'] = df['dt'].apply(lambda x : datetime.weekday(x))
        

        df['Rate'] = df['Fed. Funds Rate'].apply(helpers.split_rate)


        df = df[['Rate', 'dt', 'dow']]
        df.columns = ['Rate', 'Day', 'DayOfWeek']


        df['NextDay'] = df.apply(lambda x: helpers.N_filter(x['Day'], x['DayOfWeek']), axis = 1)
        df['PrevDay'] = df.apply(lambda x: helpers.B_filter(x['Day'], x['DayOfWeek']), axis = 1)
        return df



if __name__ == "__main__":
    #print(FFR_data.get_futures())
    print(FFR_data.get_dates())
