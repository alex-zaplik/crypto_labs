import random

from libs import utils, crypto_libs


class Oracle:

    def __init__(self):
        self.key = utils.random_bytes(16)
        self.iv = utils.random_bytes(16)
        self.mode = 'aes-128-cbc'


    def get_cypher(self, msg):
        cypher = crypto_libs.encrypt(msg, self.key, self.mode, iv=self.iv)
        self.iv = utils.increment_bytes(self.iv)
        return cypher


    def challenge(self, msg_0, msg_1):
        self.bit = random.getrandbits(1)
        if not self.bit:
            return self.get_cypher(msg_0)
        else:
            return self.get_cypher(msg_1)
    

    def test(self, bit):
        return bit == self.bit
