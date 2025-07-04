#!/usr/bin/python

import socket
from rsa_utils import load_key, decrypt_message
import time

HOST ='192.168.52.128'
PORT = 65432

private_key = load_key("sever_private.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	print("sever listening...")
	conn, addr = s.accept()
	with conn:
		print(f"connected by {addr}")
		while True:
			data = conn.recv(4096)
			if not data:
				break
			decrypted = decrypt_message(data.decode(), private_key)
			print("\n new message received!")
			print("message will self-destruct in 10 seconds:")
			print(f">>> {decrypted}")
			time.sleep(10)
			print("message deleted.\n" + "_"*40)

