# Primes: p, q | N = p*q | phi(N) = coprimes = (p-1)*(q-1) | e: 1 < e < phi(N), e is coprime of N AND phi(N) |
# d where: d*e (mod phi(N)) = 1
# Lock: (e, N), Key: (d, N)
# Encrypt given decrypted message M and encrypted message S: M^e (mod N) = S
# Decrypt given encrypted message S and decrypted message M: S^d (mod N) = M
import random
import os
import textwrap
import base64
import re


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
    print 'Started generation...'

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
        print 'Final primality check...'
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
    print 'Got Keys!'
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
    num = pow(a, n - 1, n)
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


def generate_keys(location='', key_size=2048):
    """
    Generate RSA private and public key pairs
    :param location: Where to save the keys in PEM format
    :param key_size: Size of the key in bits
    :return: public key, private key
    """
    p = generate_prime(key_size/2)
    q = generate_prime(key_size/2)
    n = q * p
    phi_n = euler_totient_function(q, p)
    e = 65537
    if not (e < phi_n and gcd(e, phi_n) == 1 and gcd(e, n) == 1):
        e = 257
        if not (e < phi_n and gcd(e, phi_n) == 1):
            print 'Failed to pick a suitable public exponent, needs implementation'
            return ''
    d = multiplicative_inverse(e, phi_n)
    public_key = (e, n)
    private_key = (d, n)
    # location = 'c:\keys'  # temp
    format_pem(public_key, location, True)
    format_pem(private_key, location, False)
    return public_key, private_key


def multiplicative_inverse(e, phi):
    """
    Return the multiplicative inverse of the public exponent e and the totient function of the modulus n
    :param e: The public exponent
    :param phi: Euler's totient function for the modulus n
    :return: The multiplicative inverse (i.e d, the private modulus)
    """
    t, newt, r, newr = 0, 1, phi, e
    while newr != 0:
        quotient = r / newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return False
    if t < 0:
        t += phi
    return t


def format_pem(key, location, is_public):
    """
    Format a given key into PEM
    :param key: The key to be formatted
    :param location: Where to save the key file
    :param is_public: Is this key the public or the private key
    :return: True for success False for failure
    """
    # codes:
    sequence = "30"
    integer = "02"
    n = add_zeroes(clean_hex(key[0]))
    exponent = add_zeroes(clean_hex(key[1]))
    n_part = integer + length_part(n) + n
    exponent_part = integer + length_part(exponent) + exponent
    to_save = sequence + length_part(n_part + exponent_part) + n_part + exponent_part
    to_save = base64.b64encode(to_save)
    if not os.path.exists(location):
        os.mkdir(location)
    if is_public:
        save_public_key(to_save, location)
    else:
        save_private_key(to_save, location)


def needs_more_bytes(num_in_hex):
    """
    A check of length for the PEM format, checks if there is a need for extra bytes to denote the length of a part
    :param num_in_hex: The number to be saved
    :return: True if there is a need for extra bytes and False if there isn't
    """
    length = len(textwrap.wrap(num_in_hex, 2))
    if length > 127:
        return True
    return False


def clean_hex(num):
    """
    Strips hex markings from a hex string
    :param num: Number as hex
    :return: Number in hex without hex markings (i.e '0x' and the long type marker, 'L' at the end)
    """
    return hex(num).strip('0x').strip('L')


def length_part(hex_num):
    """
    Creates the bytes denoting the length of a part that follows in the PEM format
    :param hex_num: The number to be in the part
    :return: Bytes representing the length of the part that follows (including extra length bytes if needed)
    """
    extra_bytes = '80'
    length = len(textwrap.wrap(hex_num, 2))
    if needs_more_bytes(hex_num):
        extra_bytes = clean_hex(int(extra_bytes, 16) + length/255 + 1 * (length % 255 != 0)) + clean_hex(length)
    else:
        extra_bytes = clean_hex(length)
    return extra_bytes


def add_zeroes(hex_num):
    """
    Hex part must start with '00' for the PEM format, when turned into an int the zeroes are removed
    :param hex_num: Number to be formatted in hex
    :return: The number with '00' at the beginning
    """
    if len(hex_num) % 2 != 0:
        hex_num = '0' + hex_num
        return hex_num
    hex_num = '00' + hex_num
    return hex_num


def save_public_key(data, location):
    """
    Saves a public key into I/O
    :param data: The key formatted in PEM
    :param location: Where to save the .key file
    :return: None
    """
    separated_pem = '\r\n'.join(textwrap.wrap(data, 64))
    with open(location + 'public_key.key', 'wb+') as pubkey:
        pubkey.write('-----BEGIN PUBLIC KEY-----\r\n' + separated_pem + '\r\n-----END PUBLIC KEY-----')


def save_private_key(data, location):
    """
    Saves a private key into I/O
    :param data: The key formatted in PEM
    :param location: Where to save the .key file
    :return: None
    """
    separated_pem = '\r\n'.join(textwrap.wrap(data, 64))
    with open(location + 'private_key.key', 'wb+') as pkey:
        pkey.write('-----BEGIN PRIVATE KEY-----\r\n' + separated_pem + '\r\n-----END PRIVATE KEY-----')


def encrypt(message, key):
    """
    Run the encryption process of RSA
    :param message: The message to be encrypted
    :param key: The RSA key to encrypt with
    :return: Base 64 of the encrypted message in hex
    """
    exponent = key[0]
    modulus = key[1]
    message = add_padding(message, modulus)
    print 'padded', message
    message = pow(message, exponent, modulus)
    return base64.b64encode(hex(message))


def decrypt(message, key):
    """
    Run the decryption process of RSa
    :param message: The encrypted message to be decrypted
    :param key: The key to decrypt with
    :return: The message in integer form
    """
    message = int(base64.b64decode(message).strip('0x').strip('L'), 16)
    exponent = key[0]
    modulus = key[1]
    message = pow(message, exponent, modulus)
    print 'after decrypt, padded', message
    message = remove_padding(message)
    return message


def get_numbers_from_message(message):
    """
    Turn a message to be encrypted to a number
    :param message: The message to be encrypted
    :return: The message in integer form
    """
    to_ret = ''
    num = 1000
    for char in message:
        to_ret += str(num + ord(char))[1:]
    to_ret = int(to_ret)
    return to_ret


def get_message_from_numbers(number):
    """
    Turn a number that was derived from a message back into a message
    :param number: The number to be converted back into a message
    :return: The original message
    """
    number = str(number)
    length = len(number)
    if length % 3 != 0:
        number = ('0' * (3 - (length % 3))) + number
    number = textwrap.wrap(number, 3)
    message = ''
    for num in number:
        message += chr(int(num))
    return message


def add_padding(message, modulus):
    """
    Add padding by PKCS1
    :param message: The message to encrypt in plain text
    :param modulus: The public modulus (for length)
    :return: Int of padded plain text message
    """
    key_size = len(clean_hex(modulus)) * 8 / 3
    size_in_bits_msg = len(clean_hex(get_numbers_from_message(message))) * 8 / 3
    size_of_padding = key_size - size_in_bits_msg
    difference = modulus - get_numbers_from_message(message)
    if difference <= 0:
        return False
    padded_msg = '02'
    ff = 'ff'
    random_part_size = (size_of_padding / 8 - 4)
    random_part = str(int(os.urandom(random_part_size).encode('hex'), 16))
    random_part = re.findall('..?', random_part)
    # [random_part[x] + random_part[x+1] for x in range(0, len(random_part), 2)]
    pad = ''
    for char in random_part:
        pad += chr(int(char))
    padded_msg += pad + ff + message  # random part size /8 because size
    # is in bytes here
    # padded_msg = int(padded_msg)
    padded_msg = get_numbers_from_message(padded_msg)
    return padded_msg

# n = 14, msg = 4, padding = 10 | 02 random ff = 10 ===> 02 | 1024 key, 128 msg == 896 padding -> 02 + 880 bits
# random + ff (896 - 2 * byte - 896 -16 = 880)


def remove_padding(message):
    """
    Remove padding by PKCS1
    :param message: Padded decrypted message
    :return: Plaint text of the encrypted message
    """
    message = get_message_from_numbers(message)
    if message[:2] != '02':
        return 'Error: not PKCS1'
    try:
        for i in range(len(message)):
            if message[i] + message[i+1] == 'ff':
                return message[i+2:]
    except IndexError:
        pass
    return 'Error: cannot find marker "ff"'
