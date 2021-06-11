import functools
import random


def duplets(hex_input: str):
    if len(hex_input) % 2 != 0:
        hex_input = '0' + hex_input
        iterable = iter(hex_input)
    while True:
        yield next(iterable) + next(iterable)


def hex_from_bytes(bytes_input: bytes):
    return bytes_input.hex()


def byte_from_hex(hex_input: str):
    return int(hex_input, base=16).to_bytes(length=1, byteorder='big')


def bytes_from_hex(hex_input: str):
    return bytearray.fromhex(hex_input)


def random_bytes(bytes_size):
    return bytes(random.getrandbits(8) for _ in range(bytes_size))


def increment_bytes(bytes_number):
    length = len(bytes_number)
    incremented_int = int.from_bytes(bytes_number, byteorder='big') + 1
    return incremented_int.to_bytes(length, byteorder='big')


def xor_bytes(left, right):
    return bytes(left_byte ^ right_byte for left_byte, right_byte in zip(left, right))
