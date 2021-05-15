import argparse
import configparser

from libs import utils
from libs import test_utils


CONFIG_DEFAULT = 'config/config.ini'


def query_stage(oracle):
    msg = utils.random_bytes(16)
    ct = oracle.get_cypher(msg)
    iv = ct[-16:]
    next_iv = utils.increment_bytes(iv)

    return utils.xor_bytes(utils.xor_bytes(msg, iv), next_iv), ct[:-16] + next_iv


def test():
    oracle = test_utils.Oracle()

    msg_0, test_val = query_stage(oracle)
    msg_1 = utils.random_bytes(16)

    ct = oracle.challenge(msg_0, msg_1)

    bit = 1
    if ct == test_val:
        bit = 0

    if oracle.test(bit):
        return 1
    else:
        return 0
    

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--config_path', '-c', help='Path to config file.', default=CONFIG_DEFAULT)
  return parser.parse_args()


def get_config(parsed_args):
    config_path = parsed_args.config_path
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['cpa']


if __name__ == "__main__":
    parsed_args = parse_arguments()
    config = get_config(parsed_args)
    
    test_count = int(config.get('test_count'))
    success_count = 0

    for _ in range(test_count):
        success_count += test()

    print(f"The attack was successful {int((success_count / test_count) * 100)}% of the time")
