import RSA


def main():
    prime = RSA.generate_prime(2048)
    print prime
    x = hex(prime).strip('0x').strip('L')
    print x
    print type(hex(prime))
    print len(x)


if __name__ == '__main__':
    main()
