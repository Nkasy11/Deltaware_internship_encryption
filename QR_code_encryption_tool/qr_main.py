#!/usr/bin/python
from qr_crypto import encrypt_to_qr, decrypt_from_qr

def main():
	print("=== QR code encryption tool ===")
	print("1. encrypt message into qr")
	print("2. decrypt message from qr")
	print("3. exit")

	choice = input(" choose an option (1/2/3): ").strip()

	if choice == '1':
		message = input("enter message or credentials to encrypt: ")
		password = input("enter encryption password: ")
		filename = input("save QR image as (e.g., secret.png): ")
		encrypt_to_qr(message, password, filename)
	elif choice == '2':
		file_path = input("enter QR image filename to decrypt: ")
		password = input("enter password: ")
		decrypt_from_qr(file_path, password)
	elif choice == '3':
		print("Goodbye!")
		exit()
	else:
		print("Invalid choice. Please try again.")

if __name__ == "__main__":
	while True:
		main()
