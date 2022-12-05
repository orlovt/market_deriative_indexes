from datetime import datetime
import pandas as pd 

from help_functions import helpers, analytical
from data import FFR_data




class Analytics():
    def __init__(self, ts, type = 'single'):
        self.ts = ts 
        self.type = type
        self.prev_ts = FFR_data.add_dates_list(self.ts)
        probs  = Analytics.f_prices(self)
        self.prev_futures_prices = probs[0]
        self.days_B_data = probs[1]
        self.df = probs[2]
        self.df_plt = probs[3]

    def f_prices(self):
        main_res = {}
        full_res = {}
        df = pd.DataFrame(columns=["Date", "EffectiveFedFundsRate", 
                                   "Hike_Low", 
                                   "Prob_Hike_Low", 
                                   "Range_Hike_Low",  
                                   "Hike_High", 
                                   "Prob_Hike_High", 
                                   "Range_Hike_High"])

        pf = pd.DataFrame(columns=["Date", "EffectiveFedFundsRate", "Type",
                                   "Hike", 
                                   "Prob_Hike", 
                                   "Range"])
                                   

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
            
            d = {"Date":strdt, "EffectiveFedFundsRate":EFFR, 
                "Hike_Low":list(dct.keys())[0], 
                "Prob_Hike_Low":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range_Hike_Low":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[1]],  
                "Hike_High":list(dct.keys())[1], 
                "Prob_Hike_High":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range_Hike_High":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[1]]}

            l = {"Date":strdt, "EffectiveFedFundsRate":EFFR, "Type":'Low', 
                "Hike":list(dct.keys())[0], 
                "Prob_Hike":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[1]]}
            
            h = {"Date":strdt, "EffectiveFedFundsRate":EFFR, "Type":'High', 
                "Hike":list(dct.keys())[1], 
                "Prob_Hike":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[1]]}
            
            df = df.append(d, ignore_index=True)
            
            pf = pf.append(l, ignore_index=True)
            pf = pf.append(h, ignore_index=True)

        return [main_res, full_res, df, pf]








if __name__ == "__main__":
    test = Analytics('2022-09-21')
    for i in test.prev_futures_prices: 
        print(i, test.prev_futures_prices[i]) #['extra']
    print(test.df)
    print(test.df_plt)
    
