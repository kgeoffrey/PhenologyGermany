from scipy import stats
from statsmodels.tsa.stattools import adfuller


def simple_t_test(mean):
    for col in mean.columns:
        dat = mean[col].dropna()
        
        fault_cols = ["Spätsommer", "Winter"]
        if col in fault_cols: # fix starting years
            dat = dat[dat.index > 1990]
            dat = dat[dat.index > 1990]
            dat = dat[dat.index > 1990]
            
        #result = adfuller(dat.values)
        slope, intercept, r_value, p_value, std_err = stats.linregress(dat.index,dat)
        print(col + '\'s slope estimate : ' + str(slope.round(5)))
        print(col + '\'s std_err : ' + str(std_err.round(5)))
        print(col + '\'s p-value : ' + str(p_value.round(10)))
        


def ADF_test(mean):
    for col in mean.columns:
        dat = mean[col].dropna()
        result = adfuller(dat.values)

        if result[0] > -3:
            dat = dat.diff().dropna()
            result = adfuller(dat.values)
            print(col + '_diff')
        else:
            print(col)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:'  + '\n')
        #print(str(result) + '\n')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value) + '\n')