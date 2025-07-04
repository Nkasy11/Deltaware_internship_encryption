import sys
import base64
import getpass
from PIL import Image
from cryptography.fernet import Fernet
import hashlib

def drive_key(password):
	return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt(data, password):
	f = Fernet(drive_key(password))
	return f.encrypt(data.encode())

def decrypt(token, password):
	f = Fernet(drive_key(password))
	return f.decrypt(token).decode()

def embed_lsb(image_path, output_path, data):
	img = Image.open(image_path)
	binary = ''.join(format(byte, '08b') for byte in data)
	pixels = img.convert('RGB').getdata()

	new_pixels = []
	idx = 0
	for pixel in pixels:
		r, g, b = pixel
		if idx < len(binary):
			r = (r & ~1) | int(binary[idx])
			idx += 1
		if idx < len(binary):
			g = (g & ~1) | int(binary[idx])
			idx += 1
		if idx < len(binary):
			b = (b & ~1) | int(binary[idx])
			idx += 1
		new_pixels.append((r, g, b))

	img.putdata(new_pixels)
	img.save(output_path, 'BMP')
	print(f"[+] Data embedded in {output_path}")

def extract_lsb(image_path, length):
	img = Image.open(image_path)
	pixels = img.convert('RGB').getdata()
	bits = ''
	for pixel in pixels:
		for color in pixel:
			bits += str(color & 1)
			if len(bits) >= length * 8:
				break
		if len(bits) >= length * 8:
			break
	data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
	return data

def main():
	if len(sys.argv) < 2:
		print("Usage:\n Hide:  python auto_steg.py hide <images.png> <text>\n Extract: python auto_steg.py extract <images.bmp> <length>")
		return

	mode = sys.argv[1]

	if mode in ['hide', 'extract']:
		image_path = sys.argv[2]
		password = getpass.getpass("enter password: ")

		if mode == 'hide':
			text = sys.argv[3]
			encrypted = encrypt(text, password)
			output_image = image_path.rsplit('.', 1)[0] + "_hidden.bmp"
			embed_lsb(image_path, output_image, encrypted)

		elif mode == 'extract':
			length = int(sys.argv[3])
			raw = extract_lsb(image_path, length)
			try:
				decrypted = decrypt(raw, password)
				print(f"[+] Extracted Text: {decrypted}")
			except Exception:
				print("[-] Decryption Failed: Wrong password or corrupted data.")
	else:
		print("invalid mode.")

if __name__ == '__main__':
	main()

