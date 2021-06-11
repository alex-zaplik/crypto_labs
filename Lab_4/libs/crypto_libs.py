import subprocess
import random
import pathlib
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Text, List

from config import settings
from libs import utils


SIZE_OF_IV = 16


def encrypt(data: bytes, secret: bytes, mode, iv: bytes = None):
    use_iv = mode != AES.MODE_ECB
    print(mode)

    if use_iv:
        iv = iv or bytes(random.randrange(0, 255) for _ in range(SIZE_OF_IV))
        cipher = AES.new(secret, mode, iv)
        return iv + cipher.encrypt(pad(data, 16))

    else:
        cipher = AES.new(secret, mode)
        return cipher.encrypt(pad(data, 16))


def decrypt(data: bytes, secret: bytes, mode):
    use_iv = mode != AES.MODE_ECB

    if use_iv:
        iv = data[:SIZE_OF_IV]
        data = data[SIZE_OF_IV:]

        cipher = AES.new(secret, mode, iv)
        return unpad(cipher.decrypt(data), 16)
        
    else:
        cipher = AES.new(secret, mode)
        return unpad(cipher.decrypt(data), 16)
