import os
import base64

from flask import current_app
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def get_cipher():
    secret=current_app.config["ENC_KEY"]
    if not secret:
        raise RuntimeError("ENC_KEY is missing")

    key=base64.b64decode(secret,validate=True)
    if len(key) !=32:
        raise RuntimeError("ENC_KEY must be 32 bytes")

    return AESGCM(key)

def encrypt_phone(phone):
    cipher=get_cipher()

    nonce=os.urandom(12)

    encrypted=cipher.encrypt(nonce,phone.encode("utf-8"),None)

    return base64.b64encode(nonce +encrypted).decode("utf-8")

def decrypt_phone(encrypted_phone):
    cipher=get_cipher()

    data=base64.b64decode(encrypted_phone)
    nonce=data[:12]
    ciphertext=data[12:]
    decrypted=cipher.decrypt(nonce,ciphertext,None)

    return decrypted.decode("utf-8")
