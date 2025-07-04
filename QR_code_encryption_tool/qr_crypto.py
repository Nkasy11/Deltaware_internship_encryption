#!/usr/bin/python

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

#padding for AES block size
def pad(data):
	return data + b' ' * (16 - len(data) % 16)

#derive a 256-bit key using PBKDF2
def derive_key(password, salt):
	return PBKDF2(password, salt, dkLen=32)

#encrypt the message, encode as QR
def encrypt_to_qr(message, password, output_file):
	salt = get_random_bytes(16)
	key = derive_key(password.encode(), salt)
	cipher = AES.new(key, AES.MODE_CBC)
	ciphertext = cipher.encrypt(pad(message.encode()))
	payload = b64encode(salt + cipher.iv + ciphertext).decode()


	qr = qrcode.make(payload)
	qr.save(output_file)
	print(f"[+] QR code saved as {output_file}")

#decrypt a QR image
def decrypt_from_qr(image_path, password):
	data = decode(Image.open(image_path))[0].data
	decoded = b64decode(data)
	salt, iv, ciphertext = decoded[:16], decoded[16:32], decoded[32:]

	key = derive_key(password.encode(), salt)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	plaintext = cipher.decrypt(ciphertext).rstrip(b' ')
	print(f"[+] decrypted message: {plaintext.decode()}")
