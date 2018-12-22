import RSA
import socket

IP = '192.168.212.200'
PORT = 8192

client_sock = socket.socket()
client_sock.connect((IP, PORT))
client_sock.send('SEND PUBLIC KEY')
public_key = client_sock.recv(4096).split(',')
public_key = [int(x) for x in public_key]
print public_key
message = raw_input('Message:\n')
encrypted_message = RSA.encrypt(message, public_key)
print encrypted_message
client_sock.send(encrypted_message)
print client_sock.recv(4096)
