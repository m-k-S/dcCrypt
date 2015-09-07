# @m-k-S
# Experimental Dirichlet convolution based encryption method

import time
import os
import binascii
import sys

def prime_factors(n):
    d = 2
    while n > 1:
        a = 0
        while (n % d) == 0:
            a += 1
            n /= d
        if a > 0:
            yield (d, a)
        d += 1

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
    divisorlist = []
    for i in get_divisors(n):
        divisorlist.append(i)
    convolvesum = 0
    for div in divisorlist:
        convolvesum = convolvesum + int(a[int(div) - 1]) * int(b[int(n / div) - 1])
    return convolvesum

    # f star g (6) = f(1)g(6) + f(2)g(3) + f(3)g(2) + f(6)g(1)

def stage1(binrep):
    binlen = len(binrep)
    sumlist = []
    if binlen % 2 == 0:
        a = binrep[0:int(binlen/2)]
        b = binrep[int(binlen/2):int(binlen)]
    else:
        a = binrep[0:int(binlen/2 - 0.5)]
        b = binrep[int(binlen/2 + 0.5):int(binlen - 2)]
    for z in range(2, binlen/4):
        summed = convolve(a, b, z)
        sumlist.append(summed)
    print sumlist
    return sumlist

def stage2(sumlist):
    hashstring = []
    for i in sumlist:
        hashstring.append(hex(i % 16)[2:])
    return ''.join(hashstring)

def stage3(hashstring):
    while len(hashstring) >= 32:
        if len(hashstring) % 32 == 0:
            stage1(hashstring)
        else:
            while len(hashstring) % 32 != 0:
                hashstring = hashstring + "0"
            stage1(hashstring)
    return hashstring

def init():
    f = open(os.getcwd() + "\\" + sys.argv[1], "rb")
    size = os.path.getsize(os.getcwd() + "\\" + sys.argv[1])
    binlist = []
    with f:
        byte = [f.read(1) for g in range(size)]
        for i in byte:
            binlist.append(ord(i))
    return binlist

print stage3(stage2(stage1(init())))
#print convolve([12,112,453,34,45,23],[32,24,360,65,56,23],6)
#print stage1(init())
