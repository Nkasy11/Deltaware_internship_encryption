#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

def generate_keys():
	key = RSA.generate(2048)
	private_key = key
	public_key = key.publickey()
	return private_key, public_key

def save_keys(private_key, public_key, prefix):
	with open(f"{prefix}_private.pem", "wb") as f:
		f.write(private_key.export_key())
	with open(f"{prefix}_public.pem", "wb") as f:
		f.write(public_key.export_key())

def load_key(path):
	with open(path, "rb") as f:
		return RSA.import_key(f.read())

def encrypt_message(message, pubkey):
	cipher = PKCS1_OAEP.new(pubkey)
	return b64encode(cipher.encrypt(message.encode())).decode()

def decrypt_message(ciphertext_b64, privkey):
	cipher = PKCS1_OAEP.new(privkey)
	data = b64decode(ciphertext_b64.encode())
	return cipher.decrypt(data).decode()
