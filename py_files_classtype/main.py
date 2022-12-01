from datetime import datetime

from help_functions import helpers, analytical
from data import FFR_data




class Analytics():
    def __init__(self, ts, type = 'single'):
        self.ts = ts 
        self.type = type
        self.prev_ts = FFR_data.add_dates_list(self.ts)
        computes_probs  = Analytics.f_prices(self)
        self.prev_futures_prices = computes_probs[0]
        self.days_B_data = computes_probs[1]

    def f_prices(self):
        main_res = {}
        full_res = {}

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

            full_res[i] = {"DT":dt, "STRDT":strdt, "FPRICE":P, 
                            "EFFR":EFFR,  "IMPL_R":IMPL, 
                            "N":N, "M":M, "WA":WA, "PH":PH, 
                            "RHIKE_PROBS":dct}

            main_res[i] = {'DT':strdt,'EFFR':EFFR,'Rate_Hikes':dct}

        return [main_res, full_res]





if __name__ == "__main__":
    test = Analytics('2022-09-21')
    for i in test.prev_futures_prices: 
        print(i, test.prev_futures_prices[i]) #['extra']
    
