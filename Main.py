import RSA
import socket
import time
import datetime

IP = '0.0.0.0'
PORT = 8192


def main():
    start_time = time.time()
    now = datetime.datetime.now()
    current_time_hour = [str(now.hour), str(now.minute), str(now.second)]
    print 'Started: [%s]' % ':'.join(current_time_hour)
    big_prime = RSA.generate_prime(size=16384)
    # public, private = RSA.generate_keys('keys\\')
    """
    message = 'Shalom'  # raw_input('Message:\n')
    print 'Encrypting'
    message = RSA.encrypt(message, public)
    print message
    print 'Decrypting'
    message = RSA.decrypt(message, private)
    print message
    """
    print big_prime
    with open('big_prime', 'wb+') as fh:
        fh.write(str(big_prime))
    # print public, private
    # print socket_stuff(public, private, IP, PORT)

    elapsed_time = round(time.time() - start_time, 5)
    print 'Done! Finished in [%ss]' % elapsed_time


def socket_stuff(public, private, ip, port):
    server_sock = socket.socket()
    server_sock.bind((ip, port))
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
