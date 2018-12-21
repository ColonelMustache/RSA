import RSA
import socket


def main():
    public, private = RSA.generate_keys('c:\keys\\', 1024)
    """
    message = 'Shalom'  # raw_input('Message:\n')
    print 'Encrypting'
    message = RSA.encrypt(message, public)
    print message
    print 'Decrypting'
    message = RSA.decrypt(message, private)
    print message
    """
    print socket_stuff(public, private)


def socket_stuff(public, private):
    server_sock = socket.socket()
    server_sock.bind(('0.0.0.0', 8192))
    server_sock.listen(5)
    print 'Running...'
    client_sock, client_address = server_sock.accept()
    print client_sock.recv(1024)
    to_send_public = str(public[0]) + ',' + str(public[1])
    client_sock.send(to_send_public)
    encrypted_message = client_sock.recv(4096)
    print encrypted_message
    decrypted = RSA.decrypt(encrypted_message, private)
    client_sock.send(decrypted)
    return decrypted


if __name__ == '__main__':
    main()
