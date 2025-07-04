#!/usr/bin/python

import socket
from rsa_utils import load_key, encrypt_message

HOST = '192.168.52.128'
PORT = 65432

sever_pub = load_key("sever_public.pem")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print("secure chat client")
	while True:
		msg = input("type a secure message(or 'exit'): ")
		if msg.lower() == 'exit':
			break
		encrypted = encrypt_message(msg, sever_pub)
		s.sendall(encrypted.encode())
