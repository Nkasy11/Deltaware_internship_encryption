#!/usr/bin/python

from rsa_utils import generate_keys, save_keys


sever_priv, sever_pub = generate_keys()
save_keys(sever_priv, sever_pub, "sever")

print("RSA keys generated and saved.")
