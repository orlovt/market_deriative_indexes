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
        def split_rate(s): # splits string of type '0.00%-0.25% into a float num 12.5 pp
            if chr(8211) in s:
                wow = s.split(chr(8211))
                s1 = wow[0][:-1]
                s2 = wow[1][:-1]
                return (float(s1) + float(s2)) / 2
            else:
                return float(s[:-1]) 

        def N_filter(dt, dow): # returns the next date markets were open for the date given 
            
                if dow >= 4: 
                    return dt + timedelta(days=(7-dow))
                else: 
                    return dt + timedelta(days=1)

        def B_filter(dt, dow): # returns the last date markets were open for the date given 
                dow = datetime.weekday(dt)
                if dow == 6: 
                    return dt - timedelta(2)
                elif dow == 5:
                    return dt - timedelta(1)
                else: 
                    return dt
                #else: 
                    #return dt - timedelta(days=1)
        def days_1_before(dt, dow):
            dt = dt - timedelta(1)
            return helpers.B_filter(dt, dow)
        def week_before(dt, dow):
            dt = dt - timedelta(7)
            return helpers.B_filter(dt, dow)
        def week_2_before(dt, dow):
            dt = dt - timedelta(14)
            return helpers.B_filter(dt, dow)
        def month_before(dt, dow):
            dt = dt - timedelta(30)
            return helpers.B_filter(dt, dow)






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

    def assing_fprices(df):
        df['PricePrevDay'] = df['PrevDay'].apply(lambda x : priceoffutures_dict[x] if x in priceoffutures_dict.keys() else 0)
    


    def get_prev_dates():
        url = 'https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[1] #current 

        #data prep and clean 
        df['dt'] = df['Date'].apply(lambda x:datetime.strptime(x, '%B %d, %Y'))
        df['dow'] = df['dt'].apply(lambda x : datetime.weekday(x))
        
        

        df = df[['Fed. Funds Rate', 'dt']]
        df.columns = ['Rate', 'Day']

        return df

    def add_columns(df):
        if 'Rate' in df.columns:
            df['Rate'] = df['Rate'].apply(helpers.split_rate)
        df['DayOfWeek'] = df['Day'].apply(lambda x : datetime.weekday(x))
        #df['NextDay'] = df.apply(lambda x: helpers.N_filter(x['Day'], x['DayOfWeek']), axis = 1)
        df['DayBefore'] = df.apply(lambda x: helpers.days_1_before(x['Day'], x['DayOfWeek']), axis = 1)
        df['1WeekBefore'] = df.apply(lambda x: helpers.week_before(x['Day'], x['DayOfWeek']), axis = 1)
        df['2WeekBefore'] = df.apply(lambda x: helpers.week_2_before(x['Day'], x['DayOfWeek']), axis = 1)
        df['MonthBefore'] = df.apply(lambda x: helpers.month_before(x['Day'], x['DayOfWeek']), axis = 1)


        return df

    def next_meeting(): #make automatic 
        date = '2022-12-14'
        d = {'Day': ['2022-12-17'], 'Rate':['3.75%–4.00%']}
        df = pd.DataFrame(d)
        df['Day'] = df['Day'].apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))
        return df
        
        



if __name__ == "__main__":
    #print(FFR_data.get_futures())
    #print(FFR_data.get_prev_dates())
    #print(FFR_data.next_meeting())
    #df = FFR_data.get_prev_dates()
    df = FFR_data.next_meeting()
    print(FFR_data.add_columns(df))
