import base64
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("AES_KEY").encode('utf-8')
iv = os.environ.get("AES_IV").encode('utf-8')


def encrypt_aes(data_message):
    data_message = pad(data_message.encode(), 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(data_message)).decode("utf-8", "ignore")


def decrypt_aes(data_encrypted):
    data_encrypted = base64.b64decode(data_encrypted)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data_encrypted), 16).decode("utf-8", "ignore")