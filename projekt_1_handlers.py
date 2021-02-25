import pandas
def emaCompute(N,startIndex, values):
    alfa = 2.0/(N+1.0)                              #setting up constants and sums variables
    den = 0
    cntr = 0
    mul = 1 - alfa
    for i in range(0,N+1,1):                    #computing counter and denominator in one loop, i=0 i_max = N
        if(startIndex-i < 0): break
        den += pow(mul,i)                       #den += (1 - alfa)^i
        cntr += pow(mul,i)*values[startIndex-i] #cntr += (1 - alfa)^i * p{i}
    return (cntr/den)

def menageStock(signal):                        #function to determine where the macd and signal lines cut
    Buy = []
    Sell = []
    flag = -1

    for i in range(0,len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i] and flag != 1:
            Buy.append(i+35)
            flag = 1
        elif signal['MACD'][i] < signal['Signal Line'][i] and flag == 1:
            Sell.append(i+35)
            flag = 0
    return (Buy, Sell)                          #returns lists of values indexes where the lines signs to buy/sell

def wprCompute(N,startIndex,values, highest, lowest):            #function to compute wpr value for N period
    hi = float('-inf')
    close = values[startIndex]
    low = float('inf')
    for i in range(0,N+1,1):
        new_h = highest[startIndex-i]
        new_l = lowest[startIndex-i]
        if(new_h > hi): hi = new_h
        if(new_l < low): low = new_l
    return ((hi - close)/(hi - low) * -100)

def smmCompute(N,startIndex,values,smmSum):     #function to compute smm value for N period
    if(len(smmSum) == 0): return values[startIndex]
    sum = values[startIndex]
    sum_b = smmSum[startIndex-1]
    for i in range(0,N,1):
        if(startIndex-i < 0):break
        sum += values[startIndex-i]
    return ((sum - sum_b) / N)

def computeAsset(macd_val, signal_val,values):
    df = pandas.DataFrame()                                 #simple algorithm to compute gains for earlier computed MACD values
    df['MACD'] = macd_val[35:]
    df['Signal Line'] = signal_val[35:]
    df['Close Value'] = values[35:]
    Buy, Sell = menageStock(df)

    Times = (Buy + Sell)
    Times.sort()

    asset_MACD = 1000
    cur_value = 0
    max_value = 0
    i = 0

    print('')
    print("Algorytm bazujący na przecięciach linii MACD oraz MACD-signal.")
    print("Kapitał początkowy: ", asset_MACD)

    for x in range(0,len(Times)):
        if(asset_MACD):
            cur_value = asset_MACD / values[Times[x]]       #stock for 1000j
            asset_MACD = 0
        elif(cur_value):
            asset_MACD = cur_value * values[Times[x]]       #j we can cash out
            if(asset_MACD > max_value): max_value = asset_MACD; i = Times[x]
            cur_value = 0
            #print(asset_MACD)
        if(x == len(Times)-2 and asset_MACD): break

    print("Kapitał: ", asset_MACD)
    print("Maxymalny kapitał kiedykolwiek: ", max_value, " w dniu próbki nr.", i)
    print('')

def assetAlg(values, highest, lowest, macd_val):
    #algorithm for auto buy/sell mechanism on stock
    #using WPR, MACD, SMM to compute through each day and decide wheter buy or sell
    wpr_val = []
    smma_val = []
    for i in range(0,len(values),1):
        wpr_val.append(wprCompute(14,i,values,highest,lowest))
        smma_val.append(smmCompute(50,i,values,smma_val))

    asset = 1000
    cur_value = 0
    last_value = asset
    max_value = 0
    i = 0
    print('')
    print("Algorytm bazujący na MACD jako wskaźniku trendu oraz pomocniczo WPR oraz SMMA, jako wskaźniki zawyżonych i zaniżonych wartości.")
    print("Kapitał początkowy: ", asset)

    for x in range(35,len(values),1):
        if(asset):                  #if we can invest
            if(values[x] > smma_val[x] and macd_val[x] < 0 and wpr_val[x-1] < -80 and wpr_val[x] > -80):
                cur_value = asset / values[x]
                asset = 0
        else:                       #if we need to cash out
            if(values[x] < smma_val[x] and macd_val[x] > 0 and wpr_val[x-1] > -20 and wpr_val[x] < -20):
                asset = cur_value * values[x]
                cur_value = 0
                last_value = asset
                if(max_value < asset): max_value = asset; i = x
    if(asset == 0):
        asset = last_value
    print("Kapitał: ", asset)
    print("Maxymalny kapitał kiedykolwiek: ", max_value, " w dniu próbki nr.", i)
    print('')