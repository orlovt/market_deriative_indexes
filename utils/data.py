import pandas as pd
import requests

import yfinance as yf
import pandas_datareader as pdr

from datetime import datetime, timedelta
from help_functions import helpers

class FFR_data_df(): 

#df
    def get_prev_dates_wiki():
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
#df
    def dfadd_columns(df):
        df['DOW'] = df['D'].apply(lambda x : datetime.weekday(x))
        if 'R' in df.columns:
            df['R'] = df['R'].apply(helpers.split_rate)
        df['1DB'] = df.apply(lambda x: helpers.days_1_before(x['D'], x['DOW']), axis = 1)
        df['1WB'] = df.apply(lambda x: helpers.week_before(x['D'], x['DOW']), axis = 1)
        df['2WB'] = df.apply(lambda x: helpers.week_2_before(x['D'], x['DOW']), axis = 1)
        #df['3WB'] 
        df['1MB'] = df.apply(lambda x: helpers.month_before(x['D'], x['DOW']), axis = 1)
        return df
#none 
    def next_meeting(): #make automatic 
        date = '2022-12-14'
        d = {'D': ['2022-12-17'], 'R':['3.75%–4.00%']}
        df = pd.DataFrame(d)
        df['D'] = df['D'].apply(lambda x:datetime.strptime(x, '%Y-%m-%d'))
        return df

class FFR_data(): 

#dict    
    def get_futures(): 
        time = datetime.now()
        start_time = datetime.strptime('2022-11-20', '%Y-%m-%d' )
        #start_time = time - timedelta(90)
        ff = yf.download("ZQ=F", start=start_time, end=time, progress=False) #start="2000-01-01", end="2022-11-09"

        ff.reset_index(inplace=True)

        ff = ff[['Date', 'Close']].copy()
        ff.columns = ['Day', 'Price']


        ff.loc[:, 'Day'] = ff['Day'].apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))


        priceoffutures_dict = {}
        for i in range(ff.shape[0]):
            priceoffutures_dict[ff['Day'][i]] = ff['Price'][i]
        return priceoffutures_dict
#dict 
    def get_EFFR(start, type):
        if type == 'now':  
            end = datetime.now()
            start = end - timedelta(90)
        elif type == 'near': 
            now = datetime.strptime(start, '%Y-%m-%d') #%Y-%m-%d
            end = now + timedelta(30)
            start = now - timedelta(30)
        elif type == 'all': 
            end = datetime.now()
            start = datetime.strptime(start, '%Y-%m-%d') #%Y-%m-%d


        df = pdr.DataReader('EFFR', 'fred', start, end)
        df.reset_index(inplace=True)
        effrdict = {}
        df['DATE'] = df['DATE'].apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))

        for i in range(df.shape[0]): 
            effrdict[df["DATE"][i]] = df["EFFR"][i]
        return effrdict
#dict 
    def add_dates_list(day):
        day = datetime.strptime(day, "%Y-%m-%d")
        return {'1DB':helpers.days_n_before(day, 1), 
                '3DB':helpers.days_n_before(day, 3), 
                '5DB':helpers.days_n_before(day, 3), 
                '1WB':helpers.days_n_before(day, 7), 
                '2WB':helpers.days_n_before(day, 14)}


        
if __name__ == '__main__':
    print(FFR_data.get_EFFR('2022-11-20', 'near'))
    p = FFR_data.get_futures()
    dt = datetime.strptime('2022-11-20', '%Y-%m-%d' )