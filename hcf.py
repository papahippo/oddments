#!/usr/bin/python3

from random import randint

def hcf(m, n):  # compute HCF (Highest Common Factor) of two integers
    m, n = sorted((m,n))
    if n % m ==0:
        return m
    else:
        return hcf(n-m, m)

def main():  # simple test program for hcf function
    for i in range(420):  # arbitrary iteration count
        m, n = randint(1, 1000), randint(1, 1000)
        print ("highest common factor of %3d and %3d is %3d"
                                       % (m,     n,   hcf(m, n))
               )

if __name__ == '__main__':
    main()
