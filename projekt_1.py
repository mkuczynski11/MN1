#%matplotlib inline                      #handling jupyter error
import pandas
from projekt_1_handlers import assetAlg, computeAsset, emaCompute, menageStock, smmCompute, wprCompute
import matplotlib.pyplot as plt
import numpy as np
wig20_input = pandas.read_csv('wig20_d.csv')            #Data, Otwarcie, Najnizszy, Najwyzszy,  Zamkniecie, Wolumen
                                                        # 0  ,     1   ,    2     ,      3    ,    4     ,    5     
c_size = len(wig20_input.columns)       #columns size
i_size = wig20_input.size // c_size     #input size(rows)

np_csv = wig20_input.to_numpy()         #numpy conversion
values = np_csv[:,4]                    #values to compute
macd_val = []
signal_val = []
lowest = np_csv[:,3]
highest = np_csv[:,2]

def showPlot():
    plt.plot(x_axis, macd_val,'b', label="MACD")            #plotting MACD and MACD-signal on each other
    plt.plot(x_axis, signal_val,'r', label="MACD-signal")       #red - MACD-signal, blue - MACD
    plt.title("MACD, MACD-signal")
    plt.xlabel("Indeks próbki")
    plt.ylabel("Wskaźnik")
    plt.legend(loc="upper left")
    axes = plt.gca()
    axes.set_xlim(x_limit)
    axes.set_ylim(y_limit)
    plt.show()

    plt.plot(x_axis, values)                               #plotting values in case to check the usage of the MACD
    plt.title("Values")
    axes = plt.gca()
    axes.set_xlim(x_limit)
    plt.show()

for i in range(0,i_size,1):            #computing macd values from 26 to the end, because we need 27 values in case to compute ema26
    ema_12 = emaCompute(12,i,values)
    ema_26 = emaCompute(26,i,values)
    macd_val.append(ema_12 - ema_26)
                                        #computing macd signal values from 9 to the end, because we need 19 values in case to compute ema9
for i in range(0, len(macd_val),1):
    ema_9 = emaCompute(9,i,macd_val)
    signal_val.append(ema_9)


x_axis = np.arange(0,len(signal_val))
x_limit = [len(signal_val)- 100, len(signal_val)-1]         #limitations to plots
y_limit = [-200,200]
                                                        
#showPlot()                                              #wrapped plotShowing into a function, normally I would consider making a function with parameters, however I only need them
                                                        #for simple visualization, therefore I don't want to focus on this too much

computeAsset(macd_val,signal_val,values)                #wrapped asset computing into a function with 3 parameters which are computed values for macd,signal and closing values
                                                        #this function is computing asset using only MACD, more in projekt_1_handlers.py file

assetAlg(values,highest,lowest,macd_val)                #wrapped my asset computing algorithm into function using 4 parameters, closing values, highest values, lowest values per day
                                                        #and computed MACD, more about this in projekt_1_handlers.py