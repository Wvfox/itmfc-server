import base64
import os.path
from os.path import splitext
from uuid import uuid4

import cv2
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from config.settings import MEDIA_ROOT, BASE_DIR

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class UUIDFileStorage(FileSystemStorage):
    """
    Creating a new unique name with uuid4.hex
    """
    @staticmethod
    def get_available_name(name, **kwargs):
        path, ext = splitext(name)
        delimiter = '/'
        if path.find('\\') != -1:
            delimiter = '\\'
        path = '/'.join(path.split(delimiter)[:-1])
        url = path + '/' + uuid4().hex + ext
        return url


def get_video_duration(path):
    # print(path)
    # create video capture object
    data = cv2.VideoCapture(path)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    # calculating duration of the video
    seconds = round(frames / fps)
    # video_time = datetime.timedelta(seconds=seconds)
    return seconds


def clear_dir_media():
    if os.path.exists(MEDIA_ROOT):
        for category in os.listdir(MEDIA_ROOT):
            for date in os.listdir(os.path.join(MEDIA_ROOT, category)):
                date_dir_path = os.path.join(MEDIA_ROOT, category, date)
                if not os.listdir(date_dir_path):
                    os.rmdir(date_dir_path)


@api_view(['GET'])
@parser_classes([JSONParser])
def get_src_file(request, media_url: str):
    """Get file from MEDIA"""
    src = open((str(BASE_DIR) + media_url), 'rb')
    return FileResponse(src)


'''--------------------------------------------------------------
========================= Cryptography ==========================
--------------------------------------------------------------'''
def encrypt_aes(source_str):
    # === Handlers ===
    cipher = Cipher(algorithms.AES(os.environ.get("AES_KEY").encode()), modes.CBC(("\x00" * 16).encode()))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    # === Encrypt ===
    data = str.encode(source_str)
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ciphertext).decode("utf-8")

def decrypt_aes(cipher_str):
    # === Handlers ===
    cipher = Cipher(algorithms.AES(os.environ.get("AES_KEY").encode()), modes.CBC(("\x00" * 16).encode()))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    # === Decrypt ===
    cipher_str_bytes = str.encode(cipher_str)
    data = base64.b64decode(cipher_str_bytes)
    decrypted_data = decryptor.update(data) + decryptor.finalize()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data.decode("utf-8")


'''--------------------------------------------------------------
========================= Pycryptodome ==========================
--------------------------------------------------------------'''
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad, pad

# def encrypt_aes(source_str):
#     # _iv = "\x00" * AES.block_size  # creates a 16 byte zero initialized string
#     generator = AES.new(os.environ.get("AES_KEY").encode(), AES.MODE_CBC, ("\x00" * AES.block_size).encode())
#     source_str_bytes = pad(source_str.encode(), AES.block_size)
#     encrypted = generator.encrypt(source_str_bytes)
#     return base64.b64encode(encrypted)
#
#
# def decrypt_aes(cipher_str):
#     # _iv = "\x00" * AES.block_size  # creates a 16 byte zero initialized string
#     generator = AES.new(os.environ.get("AES_KEY").encode(), AES.MODE_CBC, ("\x00" * AES.block_size).encode())
#     cipher_str_bytes = base64.b64decode(cipher_str)
#     decrypted = generator.decrypt(cipher_str_bytes)
#     return unpad(decrypted, AES.block_size).decode(encoding="utf-8")
