import pandas as pd
import requests

import yfinance as yf
import pandas_datareader as pdr

from datetime import datetime, timedelta
from help_functions import helpers

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
