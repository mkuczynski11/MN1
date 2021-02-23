%matplotlib inline
import pandas
from projekt_1_handlers import emaCompute
import matplotlib.pyplot as plt
import numpy as np
wig20_input = pandas.read_csv('wig20_d.csv')            #Data, Otwarcie, Najnizszy, Najwyzszy,  Zamkniecie, Wolumen
                                                        # 0  ,     1   ,    2     ,      3    ,    4     ,    5     
c_size = len(wig20_input.columns)       #columns size
i_size = wig20_input.size // c_size     #input size(rows)

np_csv = wig20_input.to_numpy()         #numpy conversion
values = np_csv[:,4]                    #values to compute

macd_val = []
for i in range(26,i_size,1):            #computing macd values from 26 to the end, because we need 27 values in case to compute ema26
    ema_12 = emaCompute(12,i,values)
    ema_26 = emaCompute(26,i,values)
    macd_val.append(ema_12 - ema_26)

signal_val = []                         #computing macd signal values from 9 to the end, because we need 19 values in case to compute ema9
for i in range(9, len(macd_val),1):
    ema_9 = emaCompute(9,i,macd_val)
    signal_val.append(ema_9)


x_axis = np.arange(0,len(signal_val))
plt.plot(x_axis, macd_val[9:])
plt.plot(x_axis, signal_val)
plt.title("MACD")
axes = plt.gca()
axes.set_xlim([len(signal_val)- 300, len(signal_val)-1])
axes.set_ylim([-200,200])
plt.show()