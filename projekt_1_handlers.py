def emaCompute(N,startIndex, values):
    alfa = 2.0/(N+1.0)                              #settign up constants and sums variables
    den = 0
    cntr = 0
    mul = 1 - alfa
    for i in range(0,N+1,1):                    #computing counter and denominator in one loop, i=0 i_max = N
        if(startIndex-i < 0): continue
        den += pow(mul,i)                       #den += (1 - alfa)^i
        cntr += pow(mul,i)*values[startIndex-i] #cntr += (1 - alfa)^i * p{i}
    return (cntr/den)