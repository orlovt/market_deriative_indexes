import pandas as pd
import numpy as np 
import requests


from calendar import monthrange
import json
import math 


import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class FFR_probs():
    def test():
        return 0

class FFR_data(): 
    def get_futures(): 
        time = datetime.now()
        start_time = time - timedelta(30)
        ff = yf.download("ZQ=F", start=start_time, end=time) #start="2000-01-01", end="2022-11-09"
        ff.reset_index(inplace=True)
        ff = ff[['Date', 'Close']]
        ff.columns = ['Day', 'Price']
        return ff

if __name__ == "__main__":
    print(FFR_data.get_futures())
