def emaCompute(N,startIndex, values):           #I assume that if input is invalid return value is min_int
    if(startIndex - N < 0): return float('-inf')
    alfa = 2/(N+1)
    den = 0
    cntr = 0
    mul = 1 - alfa
    for i in range(0,N+1,1):
        den += pow(mul,i)
        cntr += pow(mul,i)*values[startIndex-i]
    return (cntr/den)