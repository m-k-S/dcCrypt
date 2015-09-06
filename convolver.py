# @m-k-S
# Experimental Dirichlet convolution based encryption method

import time
import os
import binascii
import sys

def prime_factors(n):
    primfac = []
    d = 2
    a = 1
    while d*d <= n:
        while (n % d) == 0:
            factortuple = "("+str(d)+", "+str(a)+")"
            n //= d
            a += 1
        primfac.append(factortuple)
        d += 1
        a = 1
    if n > 1:
       primfac.append("("+str(n)+", 1)")
    return primfac

def get_divisors(n):
    factors = list(prime_factors(n))
    nfactors = len(factors)
    f = [0] * nfactors
    while True:
            yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range (nfactors)],1)
            i = 0
            while True:
                f[i] += 1
                if f[i] <= factors[i][1]:
                    break
                f[i] = 0
                i += 1
                if i >= nfactors:
                    return

# Convolves for ordered tuples given two functions with unrestricted domains
def convolve(a, b, n):
    divisorlist = get_divisors(n)
    convolvesum = 0
    for div in divisorlist:
        convolvesum = convolvesum + int(a[int(div)]) * int(b[int(n / div)])
    return convolvesum

def stage1(bin):
    binlen = len(bin)
    sumlist = []
    if binlen % 2 == 0:
        a = bin[0:int(binlen/2)]
        b = bin[int(binlen/2 + 1):int(binlen)]
    else:
        a = bin[0:int(binlen/2 - 0.5)]
        b = bin[int(binlen/2 - 0.5):int(binlen - 1)]
    print a
    print b
    for z in range(1, binlen):
        summed = convolve(a, b, z)
        sumlist.append(summed)
    return sumlist

def stage2(sumlist):
    hashstring = []
    for i in sumlist:
        v = i % 16
        if v == 0:
            hashstring.append("g")
        if v == 1:
            hashstring.append("1")
        if v == 2:
            hashstring.append("2")
        if v == 3:
            hashstring.append("3")
        if v == 4:
            hashstring.append("4")
        if v == 5:
            hashstring.append("5")
        if v == 6:
            hashstring.append("6")
        if v == 7:
            hashstring.append("7")
        if v == 8:
            hashstring.append("8")
        if v == 9:
            hashstring.append("9")
        if v == 10:
            hashstring.append("a")
        if v == 11:
            hashstring.append("b")
        if v == 12:
            hashstring.append("c")
        if v == 13:
            hashstring.append("d")
        if v == 14:
            hashstring.append("e")
        if v == 15:
            hashstring.append("f")
    ''.join(hashstring)
    return hashstring

def stage3(hashstring):
    while len(hashstring) >= 32:
        if len(hashstring) % 32 == 0:
            stage1(hashstring)
        else:
            while len(hashstring) % 32 != 0:
                hashstring + "0"
            stage1(hashstring)
    return hashstring

def init():
    f = open(os.getcwd() + "\\" + sys.argv[1], "rb")
    binpro = []
    with f:
        for g in range(1,sys.getsizeof(f)):
            byte = f.read(g)
            hexrep = binascii.hexlify(byte)
            decrep = int(hexrep, 16)
            binpro.append(decrep)
    return binpro

print stage3(stage2(stage1(init())))
