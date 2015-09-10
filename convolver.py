#
# dcCrypt - @m-k-S
# Updated 9/8/2015 at 10:42 AM GMT
# Experimental Dirichlet convolution based encryption method
#

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

# Convolves for ordered tuples given two functions with sufficient domains
def convolve(a, b, n):
    divisorlist = []
    for i in get_divisors(n):
        divisorlist.append(i)
    convolvesum = 0
    for div in divisorlist:
        convolvesum = convolvesum + int(a[int(div) - 1]) * int(b[int(n / div) - 1])
    return convolvesum


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
    return sumlist

def stage2(sumlist):
    hashstring = []
    for i in sumlist:
        hashstring.append(hex(i % 16)[2:])
    return hashstring

def stage3(hashstring):
    stringlen = len(hashstring)
    fixedhash = []
    for i in range(1,49):
        fixedhash.append(hashstring[i * (stringlen / 48)])
    return ''.join(fixedhash)

def init():
    try:
        if sys.platform == "win32" or sys.platform == "cygwin":
            f = open(os.getcwd() + "\\" + sys.argv[1], "rb")
            size = os.path.getsize(os.getcwd() + "\\" + sys.argv[1])
        else:
            f = open(os.getcwd() + "/" + sys.argv[1], "rb")
            size = os.path.getsize(os.getcwd() + "/" + sys.argv[1])
    except IOError, e:
        print "Error: %s." % e
        exit("Exiting hasher.")
    if size < 48:
        print "File too small for proper convolution."
        exit("Exiting hasher.")
    binlist = []
    with f:
        byte = [f.read(1) for g in range(size - 2)]
        for i in byte:
            if ord(i) == 13:
                pass
            else:
                binlist.append(ord(i))
    return binlist

if __name__ == "__main__":
    encrypttime = time.time()
    print stage3(stage2(stage1(init())))
    print "Algorithm finished in " + str(time.time() - encrypttime) + " seconds."
