import RSA
import textwrap
import os
import base64

public_key, private_key = RSA.generate_keys('d:\keys\\')
# public_key
# print private_key


def format_pem(key, location, is_public):
    # codes:
    sequence = "30"
    integer = "02"
    n = make_correct(clean_hex(key[1]))
    exponent = make_correct(clean_hex(key[0]))
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
    length = len(textwrap.wrap(num_in_hex, 2))
    if length > 127:
        return True
    return False


def clean_hex(num):
    return hex(num).strip('0x').strip('L')


def length_part(hex_num):
    extra_bytes = '80'
    length = len(textwrap.wrap(hex_num, 2))
    if needs_more_bytes(hex_num):
        extra_bytes = clean_hex(int(extra_bytes, 16) + length/255 + 1 * (length % 255 != 0)) + clean_hex(length)
    else:
        extra_bytes = clean_hex(length)
    return extra_bytes


def make_correct(hex_num):
    if len(hex_num) % 2 != 0:
        hex_num = '0' + hex_num
        return hex_num
    hex_num = '00' + hex_num
    return hex_num


def save_public_key(data, location):
    separated_pem = '\r\n'.join(textwrap.wrap(data, 64))
    with open(location + 'public_key.key', 'wb+') as pubkey:
        pubkey.write('-----BEGIN PUBLIC KEY-----\r\n' + separated_pem + '\r\n-----END PUBLIC KEY-----')


def save_private_key(data, location):
    separated_pem = '\r\n'.join(textwrap.wrap(data, 64))
    with open(location + 'private_key.key', 'wb+') as pkey:
        pkey.write('-----BEGIN PRIVATE KEY-----\r\n' + separated_pem + '\r\n-----END PRIVATE KEY-----')


# format_pem(public_key, 'd:\keys\\', True)
# format_pem(private_key, 'd:\keys\\', False)
print public_key
print private_key
num = 6
print 'before crypt', num
num = pow(num, public_key[0], public_key[1])
print 'after encrypt', num
num = pow(num, private_key[0], private_key[1])
print 'after decrypt', num
