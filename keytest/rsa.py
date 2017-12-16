
import random
import math

import colorama
from termcolor import colored

colorama.init()

from cryptography.hazmat.primitives.asymmetric import rsa

# Taken from rosettacode.org
def is_probable_prime(n, trials):
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)
 
    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n is definitely composite
 
    for i in range(trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
 
    return True # no base tested showed n as composite

def lcm(a,b):
    return (a*b) // math.gcd(a,b)

def test_output(prop, result):
    result_str = colored("FAIL","red")

    if result:
        result_str = colored("PASS", "green")

    print("{}: {}".format(result_str, prop))

def test_rsa(private_key, trials):
    private_numbers = private_key.private_numbers()

    p = private_numbers.p
    q = private_numbers.q
    d = private_numbers.d
    n = private_numbers.public_numbers.n
    e = private_numbers.public_numbers.e
    nlen = private_key.key_size

    test14 = is_probable_prime(p, trials)
    test15 = is_probable_prime(q, trials)
    test1 = e > pow(2, 16)
    test2 = e < pow(2, 256)
    test3 = e % 2 == 1
    
    test4 = (math.gcd(e, p-1) == 1)
    test5 = math.gcd(e, q-1) == 1

    # The square root of 2 is approximately SQRT2_A / SQRT2_B. These constants
    # are used to deal with floating point imprecision when working with huge
    # numbers.

    SQRT2_A = 665857
    SQRT2_B = 470832

    F_LOW = (pow(2, int(nlen//2) - 1) * SQRT2_A) // SQRT2_B
    F_HIGH = pow(2, int(nlen//2)) - 1
    F_DIST_LOW = pow(2, int(nlen//2) - 100)

    test6 = p > F_LOW
    test7 = p < F_HIGH
    test8 = q > F_LOW
    test9 = q < F_HIGH
    test10 = abs(p-q) > F_DIST_LOW

    D_LOW = pow(2, int(nlen//2))
    D_HIGH = lcm(p-1,q-1)

    test11 = d > D_LOW
    test12 = d < D_HIGH

    test13 = ((e*d) % D_HIGH) == 1

    test_output("e > 2^16", test1)
    test_output("e < 2^256", test2)
    test_output("e is odd", test3)
    test_output("e is coprime with p-1", test4)
    test_output("e is coprime with q-1", test5)
    test_output("p is probably prime", test14)
    test_output("q is probably prime", test15)
    test_output("p > sqrt(2) * 2^(nlen/2 - 1)", test6)
    test_output("p < 2^(nlen/2) - 1", test7)
    test_output("q > sqrt(2) * 2^(nlen/2 - 1)", test8)
    test_output("q < 2^(nlen/2) - 1", test9)
    test_output("|p-q| > 2^(nlen/2 - 100)", test10)
    test_output("d > 2^(nlen/2)", test11)
    test_output("d < LCM(p-1,q-1)", test12)
    test_output("e*d == 1 mod LCM(p-1,q-1)", test13)
