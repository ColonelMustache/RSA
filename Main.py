import RSA


def main():
    prime = RSA.generate_prime(2048)
    print prime


if __name__ == '__main__':
    main()
