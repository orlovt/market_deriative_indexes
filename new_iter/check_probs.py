from datetime import datetime, timedelta
from calendar import monthrange

from helpers import helpers
from data import FFR_data, numeric




class ffr():
    def __init__(self, ts, type = 'single'):
        self.ts = ts 
        #self.ts = datetime.strptime(ts, "%Y-%m-%d")
        self.type = type
        self.prev_ts = FFR_data.dates_list(self.ts)
        self.prev_futures_prices = ffr.f_prices(self)
    def f_prices(self):
        res1 = {}
        res2 = {}
        priceoffutures_dict = FFR_data.get_futures()
        effrdict = FFR_data.get_EFFR('', 'now')
        for i in self.prev_ts:
            dt = self.prev_ts[i]
            strdt = datetime.strftime(dt, "%Y-%m-%d")
            price = priceoffutures_dict[strdt] if strdt in priceoffutures_dict.keys() else 0
            effr = effrdict[strdt] if strdt in effrdict.keys() else 0
            impl_rate = 100 - price
            ffstart = numeric.averageoverspan(dt, priceoffutures_dict)
            N = helpers.N(dt)
            M = helpers.M(dt)
            fffin = N/(N-M) * (impl_rate- (M/N)*ffstart)
            phike =  (fffin - ffstart)/.25
            phike2 = (impl_rate -((N/(N-M))* (impl_rate - (M/N) * effr)))/.25
            res1[i] = {'dt':dt, 'impl_r':impl_rate, 'effr': effr, 'ffstart':ffstart, 'fffin':fffin, 'phike':phike, 'exphike':phike*0.25}
            
            res2[i] = {'dt':dt, 'impl_r':impl_rate, 'effr': effr, 'ffstart':ffstart, 'fffin':fffin, 'phike':phike2, 'exphike':phike2*0.25}
        return [res1, res2]





if __name__ == "__main__":
    #print(FFR_data.get_futures())
    #print(FFR_data.get_prev_dates())
    #print(FFR_data.next_meeting())
    #df = FFR_data.get_prev_dates()
    #priceoffuturesdict = FFR_data.get_futures()
    #df = FFR_data.next_meeting()
    #df = FFR_data.add_columns(df)
    #print(df)
    #print(FFR_probs.add_prices(df, '2022-12-17'))
    test = ffr('2022-11-02')
    #print(test.ts)
    #print(test.prev_ts)
    #print(test.prev_futures_prices['1DB'])
    #print(test.prev_futures_prices['1WB'])
    #print(test.prev_futures_prices['2WB'])
    #print(test.prev_futures_prices['1MB'])
    print(test.prev_futures_prices[0]['1DB'])
    print(test.prev_futures_prices[1]['1DB'])
    
    print(test.prev_futures_prices[0]['1WB'])
    print(test.prev_futures_prices[1]['1WB'])
    
    print(test.prev_futures_prices[0]['2WB'])
    print(test.prev_futures_prices[1]['2WB'])

    print(test.prev_futures_prices[0]['1MB'])
    print(test.prev_futures_prices[1]['1MB'])
    #print(test.prev_futures_prices)
    #print(FFR_data.get_EFFR('', '', 'now'))




