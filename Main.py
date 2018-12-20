import RSA


def main():
    public, private = RSA.generate_keys('d:\keys\\', 1024)
    message = 'Shalom'  # raw_input('Message:\n')
    print 'Encrypting'
    message = RSA.encrypt(message, public)
    print message
    print 'Decrypting'
    message = RSA.decrypt(message, private)
    print message


if __name__ == '__main__':
    main()
