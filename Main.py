import RSA


def main():
    prime = RSA.generate_prime(2048)
    print prime
    print hex(prime)
    print type(hex(prime))
    x = hex(prime).strip('0x').strip('L')
    print len(x)


if __name__ == '__main__':
    main()
