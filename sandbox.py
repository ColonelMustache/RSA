import os
import random
import time

"""
try:
    print 'Hi!'
    a = random.randint(0, x - 2)
    print a
    print 'Hi again!'
    print x - a
    print 'Hi thrice!'
except Exception, ex:
    print ex
    
should_loop = not fermat_primal_test(x, 10)
print 'Generated number x is prime:', should_loop
if should_loop:
"""


def fermat_primality_test(prime, num_of_tries):
    for _ in xrange(num_of_tries):
        # Get base of power
        a = random.randint(0, prime - 2)
        if not fermat_theorem(a, prime):
            return False  # not prime (certain)
    return True  # finished running, probably prime by the test


def fermat_theorem(a, n):
    """
    Does the Fermat theorem for a and n
    :param a: base
    :param n: number to check
    :return: return true if theorem holds true, false otherwise
    """
    # print 'Starting calc...'
    num = pow(a, n - 1, n)
    # print num
    if num == 1:
        return True
    return False


def pascal_triangle(n):
    """
    Calculates the values of the nth row of Pascal's triangle using the identity: C(n,k+1) = C(n,k) * (n-k) / (k+1)
    :param n: Number of the row in Pascal's trianlge to be calculated
    :return:
    """
    line = [1]
    k = 0
    while k < n:
        line.append(line[k] * (n-k) / (k+1))
        k += 1
    # for k in range(n):
    #    line.append(line[k] * (n-k) / (k+1))
    return line


def aks_test(n):
    coefficients = pascal_triangle(n)
    coefficients = coefficients[1:len(coefficients)-1]  # remove the ones on the sides
    for c in coefficients:
        if c % n != 0:
            return False
    return True


def main():
    start_time = time.time()


    print (os.path.dirname(__file__) + '/').replace('/', '\\')
    msg = 'Shalom'
    msg_uni = msg.encode('utf-8')
    print msg
    print msg_uni
    x = hex(20)
    print x
    print hex(int(x, 16) + 16)
    print range(1, 34)
    number_of_bits = 4096
    """
    x = int(os.urandom(number_of_bits/8).encode('hex'), 16)
    if x % 2 == 0:
        x += 1
        print 'Added one to make odd...'
    print 'Initial x:\n', x

    while not fermat_primality_test(x, 100):
        x += 2

    print 'Existed loop, got number:\n', x
    print 'Generated number x is prime (last check):', fermat_primality_test(x, 200)
    """
    count = 1
    for i in xrange(100000):
        count += 1
    elapsed_time = round(time.time() - start_time, 5)
    print 'Done! Finished in [%ss]' % elapsed_time


if __name__ == '__main__':
    main()
