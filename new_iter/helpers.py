from datetime import datetime, timedelta
from calendar import monthrange

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


        def days_1_before(dt):
            dt = dt - timedelta(1)
            return helpers.B_filter(dt)
        def days_3_before(dt):
            dt = dt - timedelta(3)
            return helpers.B_filter(dt)
        def days_5_before(dt):
            dt = dt - timedelta(5)
            return helpers.B_filter(dt)
        def week_before(dt):
            dt = dt - timedelta(7)
            return helpers.B_filter(dt)
        def week_2_before(dt):
            dt = dt - timedelta(14)
            return helpers.B_filter(dt)
        def month_before(dt):
            dt = dt - timedelta(30)
            return helpers.B_filter(dt)

        def M(dt): 
            return monthrange(dt.year, dt.month)[1]
        def N(dt): 
            return dt.day -1

        def mtype(dt, prev, next):             
            return None

if __name__ == "__main__": 
    dt = datetime.strptime('2022-11-20', '%Y-%m-%d' )
    print(helpers.N(dt))
    print(helpers.M(dt))