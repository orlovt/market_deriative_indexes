from datetime import datetime, timedelta
from calendar import monthrange
import math

class helpers():
        def split_rate(s): # splits string of type '0.00%-0.25% into a float num 12.5 pp for #(DF) -->  str 
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

        def B_filter(dt): # returns the last date markets were open for the date given 
                dow = datetime.weekday(dt)
                if dow == 6: 
                    return dt - timedelta(2)
                elif dow == 5:
                    return dt - timedelta(1)
                else: 
                    return dt


        def days_n_before(dt, n):
            dt = dt - timedelta(n)
            return helpers.B_filter(dt)

        def M(dt): 
            return monthrange(dt.year, dt.month)[1]
        def N(dt): 
            return dt.day -1

        def mtype(dt, prev, next):             
            return None

class analytical():
    def __init__(self, dt, EFFR, PH): 
        self.DT = dt
        self.EFFR = EFFR
        self.PH = PH

        self.probs = self.prob_tree()
    
    def prob_tree(self): 
        
        res = {}
        
        low_EFFR = math.floor(self.EFFR / .25) * 0.25
        up_EFFR = low_EFFR + 0.25

        lower_hike = math.floor(self.PH) * 0.25
        upper_hike = lower_hike + 0.25
        

        P_upper = round(self.PH % 1, 2)
        P_lower = round(1- P_upper, 2)


        lower_range = f'{low_EFFR + lower_hike}%-{up_EFFR + lower_hike}%'
        upper_range = f'{low_EFFR + upper_hike}%-{up_EFFR + upper_hike}%'

        res[lower_hike] = {'P':P_lower, 'R':lower_range}
        res[upper_hike] = {'P':P_upper, 'R':upper_range}

        return res 
    
    def get_probs(self):
        return self.probs

     


        




          
        

if __name__ == "__main__": 

    dt = datetime.strptime('2022-11-20', '%Y-%m-%d' )
    #print(helpers.N(dt))
    #print(helpers.M(dt))
    #test1 = analytical("2022-07-27", 1.58, 5.166666666666667)
    #print(test1.get_probs())