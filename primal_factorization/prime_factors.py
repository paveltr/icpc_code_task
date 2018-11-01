from math import sqrt
from itertools import count, islice
import sys
import itertools
import random
from math import gcd
from concurrent import futures
from functools import reduce



def sieve(n):
    "Returns all primes <= n."
    np1 = n + 1
    s = list(range(np1)) # leave off `list()` in Python 2
    s[1] = 0
    sqrtn = int(round(n**0.5))
    for i in range(2, sqrtn + 1): # use `xrange()` in Python 2
        if s[i]:
            # next line:  use `xrange()` in Python 2
            s[i*i: np1: i] = [0] * len(range(i*i, np1, i))
    return filter(None, s)

global primes_factors, smallprimes

# list of all possible prime factors
primes_factors = tuple(sieve(int(sqrt(2*10**9-1))))

# tuple of all primes under 1000
smallprimes = tuple(sieve(10**3))

def isPrime(n):
    """
    Checks if n is prime
    """
    if n < 2 or n == 4:
        return False
    if n == 2:
        return True
    limit = int(sqrt(n))
    for number in primes_factors:
        if number > limit:
            return True
        else:
            if n % number == 0:
                return False

    return True


def pollardBrent(n):
    """
    Returns prime factor for n
    """
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break

    return g

def bigFactors(n, sort = False):
    """
    Returns list of prime factors for a given n when n is big
    """
    factors = []
    while n > 1:
        if isPrime(n):
            factors.append(n)
            break
        factor = pollardBrent(n) 
        factors.extend(primeFactorsFast(factor, sort)) # recurse to factor the not necessarily prime factor returned by pollard-brent
        n //= factor

    if sort: factors.sort()    
    return factors

def primeFactorsFast(n, sort=False):
    """
    Returns list of prime factors for a given n
    """
    factors = []

    limit = int(n ** .5) + 1
    for checker in smallprimes:
        if checker > limit: break
        while n % checker == 0:
            factors.append(checker)
            n //= checker


    if n < 2: return factors
    else : 
        factors.extend(bigFactors(n,sort))
        return factors
    

def processPrime(n):
    """
    Process prime reduction
    """
    n = int(n)
    if n == 4 or n < 2:
        pass
    elif isPrime(n):
        return str(n) + ' 1'
    else:
        count = 2
        sum_factors = n
        while True:
            factors = primeFactorsFast(sum_factors)
            sum_factors = sum(factors)
            if isPrime(sum_factors):
                return str(sum_factors) + ' ' + str(count)
                break
            count += 1

result = ''
for line in sys.stdin:
    func_result = processPrime(int(line))
    if func_result:
        result += func_result + '\n'

sys.stdout.write(result)