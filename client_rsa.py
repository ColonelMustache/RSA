import RSA
import socket

client_sock = socket.socket()
client_sock.connect(('10.200.200.111', 8192))
client_sock.send('Ahalan!')
public_key = client_sock.recv(4096).split(',')
public_key = [int(x) for x in public_key]
print public_key
message = raw_input('Message:\n')
encrypted_message = RSA.encrypt(message, public_key)
print encrypted_message
client_sock.send(encrypted_message)
print client_sock.recv(4096)