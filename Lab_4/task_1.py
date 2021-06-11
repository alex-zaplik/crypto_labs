import argparse
import configparser
import pathlib
import hashlib
import sys
import random
import os

from Crypto.Cipher import AES

from libs import crypto_libs
from libs import keystore_libs
from libs import utils


MODES_CHOICES = ('cbc', 'ecb', 'ofb')
MODES_MAP = { 'cbc': AES.MODE_CBC, 'ecb': AES.MODE_ECB, 'ofb': AES.MODE_OFB }

OPERATION_ENC = 'enc'
OPERATION_DEC = 'dec'
OPERATION_CHOICES = (OPERATION_DEC, OPERATION_ENC)

OUTPUT_STDOUT = object()
CONFIG_DEFAULT = 'config/config.ini'


def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('operation', choices=OPERATION_CHOICES, default=OPERATION_ENC)
    parser.add_argument('--challenge', action='store_true')
    parser.add_argument('--mode', '-m', choices=MODES_CHOICES, help='Mode of encryption to be used.', default=MODES_CHOICES[0])

    parser.add_argument('--input_folder', help="Path to input data folder.")
    parser.add_argument('--output_folder', help="Name of output data folder.")
    parser.add_argument('--config_path', '-c', help='Path to config file.', default=CONFIG_DEFAULT)

    return parser.parse_args()


def get_data(parsed_args):
    if parsed_args.input_path:
        return pathlib.Path(parsed_args.input_path).read_bytes()
    return sys.stdin.buffer.read()


def get_secret(parsed_args):
    if parsed_args.config_path:
        config = configparser.ConfigParser()
        config.read(parsed_args.config_path)
        credentials_config = config['credentials']

        keystore_path = credentials_config.get('keystore')
        password = credentials_config['password']

        privkey = keystore_libs.load_key_from_keystore(keystore_path, password)
        
        return hashlib.sha512(privkey).digest()[:16]
    return utils.bytes_from_hex(input())


def get_mode(parsed_args):
    return MODES_MAP[parsed_args.mode]


def get_operation(parsed_args):
    operation = parsed_args.operation
    if operation == OPERATION_DEC:
        return crypto_libs.decrypt
    else:
        return crypto_libs.encrypt


def get_output(parsed_args):
    if parsed_args.output_path:
        return parsed_args.output_path
    return OUTPUT_STDOUT


def write_output(result, output_target):
    if output_target == OUTPUT_STDOUT:
        os.write(sys.stdout.fileno(), result)
    else:
        pathlib.Path(output_target).write_bytes(result)


def challenge(parsed_args, secret, mode, operation, files, output_folder):
    if len(files) > 2:
        print(f"Found {len(files)} files, expected 2.")
        return

    data_file = random.choice(files)
    data = data_file.read_bytes()
    result = operation(data, secret, mode)
    pathlib.Path(output_folder, "challenge").write_bytes(result)


def oracle(secret, mode, operation, files, output_folder):
    for file_name in files:
        input_data = file_name.read_bytes()
        output_data = operation(input_data, secret, mode)
        pathlib.Path(output_folder, file_name.name).write_bytes(output_data)


if __name__ == "__main__":
    parsed_args = parse_arguments()
    secret = get_secret(parsed_args)
    mode = get_mode(parsed_args)
    operation = get_operation(parsed_args)

    input_folder = pathlib.Path(parsed_args.input_folder)
    output_folder = pathlib.Path(input_folder.parent, parsed_args.output_folder)
    output_folder.mkdir()

    files = [file_name for file_name in input_folder.iterdir() if file_name.is_file()]

    if parsed_args.challenge:
        challenge(parsed_args, secret, mode, operation, files, output_folder)
    else:
        oracle(secret, mode, operation, files, output_folder)
