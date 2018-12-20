# Primes: p, q | N = p*q | phi(N) = coprimes = (p-1)*(q-1) | e: 1 < e < phi(N), e is coprime of N AND phi(N) |
# d where: d*e (mod phi(N)) = 1
# Lock: (e, N), Key: (d, N)
# Encrypt given decrypted message M and encrypted message S: M^e (mod N) = S
# Decrypt given encrypted message S and decrypted message M: S^d (mod N) = M
import random
import os
import textwrap


def generate_prime(size=1024, num_of_tries=100, max_tries=10):
    """
    Generates a prime number
    :param size: Size in bits of the prime to be generated. Default: 1024 bits.
    :param num_of_tries: How many Fermat primality tests are to be run when the test function is called. Default: 100.
    :param max_tries: How many times the 'get_prime' function (the while loop of getting a prime) should be run.
                      Keep a low number for efficiency! Default: 10.
    :return: Either a probable prime (most cases) or a false if it couldn't generate a prime in the amount of tries
             tries specified
    """
    x = int(os.urandom(size/8).encode('hex'), 16)
    if x % 2 == 0:
        x += 1
        # Added one to make odd...

    def get_prime(num):
        while not fermat_primality_test(num, num_of_tries):
            num += 2
        return num

    count = 0
    for _ in xrange(max_tries):
        x = get_prime(x)
        print 'Final check...'
        if fermat_primality_test(x, num_of_tries) and miller_rabin_test(x, num_of_tries):
            # Got sufficient probability of primality
            break
        else:
            count += 1
            print 'Check failed... Trying another prime. %s more times to run.' % (max_tries - count)
    if count == max_tries:
        if not fermat_primality_test(x, 100):
            return False  # This means the for loop ran the maximal amount of times so we check if the last run got a
            # prime by chance and it should be tested, if it wasn't prime the function is done and didn't get a prime
            # so it returns 'False'.
    print 'Success!'
    return x


def fermat_primality_test(prime, num_of_tries):
    """
    Run Fermat's primality test, done by using Fermat's little theorem
    :param prime:
    :param num_of_tries:
    :return:
    """
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


def miller_rabin_test(prime, num_of_tries=100):
    """
    Runs the Miller-Rabin primality test
    :param prime: Number to test primality of
    :param num_of_tries: Amount of times to run the test, higher means higher probabilty of primality
    :return: False if not prime (100% probabilty) or True if probably a prime
    """
    if prime == 2:
        return True
    if prime % 2 == 0:
        return False  # If a number is even it's not prime unless it's 2
    if prime == 1:
        return False  # One isn't prime...
    r, d = get_miller_rabin_components(prime - 1)
    for _ in xrange(num_of_tries):
        if not miller_rabin_calc(d, r, prime):
            return False
    return True


def miller_rabin_calc(d, r, n):
    """
    Does the calculation for the Miller-Rabin test
    :param d: Integer d such that n-1 = d*(2^r)
    :param r: Integer as above
    :param n: The number to be tested for primality
    :return: False if not prime, True if probable prime
    """
    a = random.randint(2, n - 1)  # [2, n-2] | This is inclusive of edge values
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in xrange(r-1):
        x = pow(x, 2, n)
        if x == n-1:
            return True
    return False


def get_miller_rabin_components(num):
    """
    Gets number d and r such that d*(s^r) = num.
    :param num: The number to be tested for primality minus 1. Notably always odd so the returned r is never 0.
    :return: Tuple comprised out of (r, d).
    """
    if num % 2 == 0:
        to_ret = get_miller_rabin_components(num / 2)
        return to_ret[0]+1, to_ret[1]
    # if got here then we have reached the "odd root" of the number
    return 0, num


def gcd(a, b):
    """
    Return the Greatest Common Denominator of the numbers a and b
    :param a: Number a
    :param b: Number b
    :return: Return the GCD
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def euler_totient_function(q, p):
    """
    Does the Euler totient function
    :param q: Factor 1
    :param p: Factor 2
    :return: The number of coprimes to the number q*p
    """
    return (p - 1) * (q - 1)


def create_keys(key_size, location):
    p = generate_prime(key_size/2)
    q = generate_prime(key_size/2)
    n = q * p
    phi_n = euler_totient_function(q, p)
    e = 65537
    if not (e < phi_n and gcd(e, phi_n) == 1):
        e = 257
        if not (e < phi_n and gcd(e, phi_n) == 1):
            print 'Failed to pick a suitable public exponent, needs implementation'
            return ''
    t = random.randrange(5, 10)
    d = 1/e + t * phi_n
    public_key = (e, n)
    private_key = (d, n)
    # location = 'c:\keys'  # temp
    format_pem(public_key, location, True)
    format_pem(private_key, location, False)


def format_pem(key, location, is_public):
    # codes
    SEQUENCE = "0x30"
    EXTRA_LEN_BYTES = "0x80"
    INTEGER = "0x02"
    exponent = textwrap.wrap(key[0].strip('0x').strip('L'), 2)
    exponent_part = INTEGER + hex(int(EXTRA_LEN_BYTES, 16) + len(exponent)) * (len(exponent) > 127) + ''.join(exponent)
    key_file_header = SEQUENCE + hex(int(EXTRA_LEN_BYTES, 16) + )
    if is_public:
        pass
    pass  # will save keys as PEM format in *file_name*.key


def if_needs_extra_bytes(len_int):
    if len_int > 127:
        return True
    return False
