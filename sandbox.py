import os
import random
x = int(os.urandom(1024/8).encode('hex'), 16)
print x


def fermat_primal_test(prime, num_of_tries):
    for i in num_of_tries:
        pass


def fermat_theorem(a, n):
    """
    Does the Fermat theorem for a and n
    :param a: base
    :param n: number to check
    :return: return true if theorem holds true, false otherwise
    """
    print 'Starting calc...'
    num = fast_power(a, n - 1, n)
    print num
    if num == 1:
        return True
    return False


def fast_power(base, exp, mod):
    return pow(base, exp / 2, mod)


print fermat_theorem(6, 17)
print 'done with 1'
print fermat_theorem(2, x)
print 'finished with 2'
