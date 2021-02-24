def emaCompute(N,startIndex, values):           #I assume that if input is invalid return value is min_int
    if(startIndex - N < 0): return float('-inf')
    alfa = 2/(N+1)                              #settign up constants and sums variables
    den = 0
    cntr = 0
    mul = 1 - alfa
    for i in range(0,N+1,1):                    #computing counter and denominator in one loop, i=0 i_max = N
        den += pow(mul,i)                       #den += (1 - alfa)^i
        cntr += pow(mul,i)*values[startIndex-i] #cntr += (1 - alfa)^i * p{i}
    return (cntr/den)