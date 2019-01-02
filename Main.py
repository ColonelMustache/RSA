import RSA
import socket
import time
import datetime

IP = '0.0.0.0'
PORT = 8192


def main():
    start_time = timer()
    public, private = RSA.generate_keys('keys\\', key_size=1024)
    e_msg = RSA.encrypt('hello', public)
    print e_msg
    d_msg = RSA.decrypt(e_msg, private)
    print d_msg
    """
    prime1 = RSA.generate_prime(256)
    prime2 = RSA.generate_prime(256)
    n = prime1 * prime2
    padded_msg = RSA.add_padding('hello', n)
    print 'n      ', n
    print 'padding', padded_msg
    print RSA.get_message_from_numbers(padded_msg)
    print 'removed', RSA.remove_padding(padded_msg)
    if n > int(padded_msg):
        print 'Gucci'
    else:
        print 'Oh...'
    # big_prime = RSA.generate_prime(size=2048)
    # public, private = RSA.generate_keys('keys\\')
    """
    """
    message = 'Shalom'  # raw_input('Message:\n')
    print 'Encrypting'
    message = RSA.encrypt(message, public)
    print message
    print 'Decrypting'
    message = RSA.decrypt(message, private)
    print message
    """
    # print big_prime
    # open('big_prime', 'wb+') as fh:
    # fh.write(str(big_prime))
    # print public, private
    # print socket_stuff(public, private, IP, PORT)

    elapsed_time = round(time.time() - start_time, 5)
    print 'Done! Finished in [%ss]' % elapsed_time


def timer():
    start_time = time.time()
    now = datetime.datetime.now()
    current_time_hour = [str(now.hour), str(now.minute), str(now.second)]
    print 'Started: [%s]' % ':'.join(current_time_hour)
    return start_time


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
