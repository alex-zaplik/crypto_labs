import subprocess
import random
import pathlib
import os
import OpenSSL

from typing import Text, List

from config import settings
from libs import utils


SIZE_OF_IV = 16


def encrypt(data: bytes, secret: bytes, mode: Text, iv: bytes = None):
    use_iv = mode != 'aes-128-ecb'

    if use_iv:
        iv = iv or bytes(random.randrange(0, 255) for _ in range(SIZE_OF_IV))

        command = f"openssl enc -e -{mode} -K {utils.hex_from_bytes(secret)} -iv {utils.hex_from_bytes(iv)}"
        process = subprocess.run(['bash', '-c', command], input=data, stdout=subprocess.PIPE)

        return process.stdout + iv
    else:
        command = f"openssl enc -e -{mode} -K {utils.hex_from_bytes(secret)}"
        process = subprocess.run(['bash', '-c', command], input=data, stdout=subprocess.PIPE)

        return process.stdout


def decrypt(data: bytes, secret: bytes, mode: Text):
    use_iv = mode != 'aes-128-ecb'

    if use_iv:
        iv = data[-SIZE_OF_IV:]
        data = data[:-SIZE_OF_IV]

        command = f"openssl enc -d -{mode} -K {utils.hex_from_bytes(secret)} -iv {utils.hex_from_bytes(iv)}"
        process = subprocess.run(['bash', '-c', command], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.stderr:
            return os.urandom(16)
        return process.stdout
    else:
        command = f"openssl enc -d -{mode} -K {utils.hex_from_bytes(secret)}"
        process = subprocess.run(['bash', '-c', command], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.stderr:
            return os.urandom(16)
        return process.stdout
