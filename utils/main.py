from datetime import datetime
import pandas as pd 

from help_functions import helpers, Probabilies
from data import FFR_data




class Analytics():
    '''

    '''
    def __init__(self, ts, type = 'single'):
        self.ts = ts 
        self.type = type
        self.prev_ts = FFR_data.add_dates_list(self.ts)
        probs  = Analytics.f_prices(self)
        self.prev_futures_prices = probs[0]
        self.days_B_data = probs[1]
        self.df = probs[2]
        self.df_plt = probs[3]
        self.test = probs[4]
        self.simple = probs[5]
    def get_prob_dist_df(self): #returns the df object
        return self.df
    def get_prob_dsit_df_2(self): #retutns plotting df object 
        return self.df_plt
    def get_prob_dist_dict(self): #dictionary with previous days hikke rate probability distributions 
        return self.days_B_data

    def f_prices(self):
        '''
        Defines 4 objects and budles them in a list 
        
        1. 
        2. 
        3. 
        4. 

        
        '''

        main_res = {}
        full_res = {}
        t = {}
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
        sim_df = pd.DataFrame(columns=['MD',"TD","IMPL","R_new","EXPHIKE"])
                                   

        priceoffutures_dict = FFR_data.get_futures()
        effrdict = FFR_data.get_EFFR('2015-01-01')

        for i in self.prev_ts:
            
            dt = self.prev_ts[i]
            strdt = datetime.strftime(dt, "%Y-%m-%d")
            
            P = priceoffutures_dict[strdt] if strdt in priceoffutures_dict.keys() else 0
            EFFR = (effrdict[strdt] if strdt in effrdict.keys() else 0) + 0.045
            IMPL = 100 - P

            N = helpers.N(dt)
            M = helpers.M(dt)

            WA = N/M * EFFR + (M-N)/M *IMPL
            PH = (IMPL - EFFR)/(WA - EFFR)

            #PH2 = M/(M-N) * IMPL/(N * EFFR)

            PH3 = M/(M-N) * IMPL/EFFR

            R_new = (IMPL - (N/M) * EFFR) * (M/(M-N))



            dct = Probabilies(dt, EFFR, PH3).get_probs()

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
            
            simple_row = {'MD':self.ts, "TD":dt, "IMPL":IMPL, "R_new":R_new, "EXPHIKE":R_new - EFFR}

            l = {"Date":strdt, "EffectiveFedFundsRate":EFFR, "Type":'Low', 
                "Hike":list(dct.keys())[0], 
                "Prob_Hike":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range":dct[list(dct.keys())[0]][list(dct[list(dct.keys())[0]].keys())[1]]}
            
            h = {"Date":strdt, "EffectiveFedFundsRate":EFFR, "Type":'High', 
                "Hike":list(dct.keys())[1], 
                "Prob_Hike":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[0]], 
                "Range":dct[list(dct.keys())[1]][list(dct[list(dct.keys())[0]].keys())[1]]}

            t[i] = { "STRDT":strdt,
                            "EFFR":EFFR,  "IMPL_R":IMPL, 
                            "PH3":PH3, "RH":dct
                             
                                }
                            #"RHIKE_PROBS":dct}


            sim_df = sim_df.append(simple_row, ignore_index = True)
            df = df.append(d, ignore_index=True)
            
            pf = pf.append(l, ignore_index=True)
            pf = pf.append(h, ignore_index=True)

        return [main_res, full_res, df, pf, t, sim_df]


    def simple_df(self, ts): 
            
        return None









if __name__ == "__main__":
    #test = Analytics('2022-11-02')
    #for i in test.test: 
        #print(i, test.test[i])
    #print(test.df)
    #print(test.df_plt)

    test2 = Analytics('2022-11-02')
    #for i in test2.test: 
    #    print(i, test2.test[i])
    #print(test2.df)
    #print(test2.df_plt)
    print(test2.simple)


    
