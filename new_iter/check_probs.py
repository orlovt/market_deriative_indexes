from datetime import datetime, timedelta
from calendar import monthrange

from helpers import helpers, analytical
from data import FFR_data




class ffr():
    def __init__(self, ts, type = 'single'):
        self.ts = ts 
        #self.ts = datetime.strptime(ts, "%Y-%m-%d")
        self.type = type
        self.prev_ts = FFR_data.add_dates_list(self.ts)
        self.prev_futures_prices = ffr.f_prices(self)

    def f_prices(self):
        res = {}

        priceoffutures_dict = FFR_data.get_futures()
        effrdict = FFR_data.get_EFFR('2015-01-01', 'all')

        for i in self.prev_ts:
            
            dt = self.prev_ts[i]
            strdt = datetime.strftime(dt, "%Y-%m-%d")
            
            P = priceoffutures_dict[strdt] if strdt in priceoffutures_dict.keys() else 0
            
            EFFR = effrdict[strdt] if strdt in effrdict.keys() else 0
            IMPL = 100 - P

            N = helpers.N(dt)
            M = helpers.M(dt)
            WA = N/M * EFFR + (M-N)/M *IMPL
            PH = (IMPL - EFFR)/(WA - EFFR)

            dct = analytical(dt, EFFR, PH).prob_tree()

            res[i] = {'DT':dt, 'IMPL':IMPL, 'EFFR': EFFR, 'WA':WA, 'PH':PH, 'EH':PH*0.25, 'extra':dct }
        return res





if __name__ == "__main__":
    test = ffr('2022-07-27')
    for i in test.prev_futures_prices: 
        print(i, test.prev_futures_prices[i]['extra'])
    
