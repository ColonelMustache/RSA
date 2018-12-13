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
    if (a**(n-1)) % n == 1:
        return True
    return False


print fermat_theorem(6, 17)
print 'done with 1'
print fermat_theorem(2, x)
print 'finished with 2'
