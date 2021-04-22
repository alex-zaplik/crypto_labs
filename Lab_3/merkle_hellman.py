import math
import collections

from Crypto.Random import random


PrivateKey = collections.namedtuple('PrivateKey', 'W q r inv_r n')


def generate(n):
    # Private key generation

    W = []

    s = 0
    for i in range(n * 8):
        r = random.randint(2 ** 8, 2 ** 16)
        W.append(s + r)
        s += W[i]

    q = random.randint(s + 1, 2 * s)

    r = q
    while math.gcd(r, q) != 1:
        r = random.randint(2, q - 2)

    priv_key = PrivateKey(W, q, r, pow(r, -1, q), n * 8)

    # Public key generation

    pub_key = [(r * w) % q for w in W]

    return priv_key, pub_key


def enc(msg, pub_key):
    msg_bits = list(map(int, bin(int(msg.hex(), base=16))[2:]))
    if len(msg_bits) % 8 != 0:
        msg_bits = [0] * (8 - (len(msg_bits) % 8)) + msg_bits

    return sum([msg_bits[i] * pub_key[i] for i in range(len(msg_bits))])


def dec(cypher, priv_key):
    c_prime = (cypher * priv_key.inv_r) % priv_key.q
    if c_prime < 0:
        c_prime += priv_key.q

    # TODO: Subset sum problem
    X = []

    for w in reversed(priv_key.W):
        if w <= c_prime:
            X.append(1)
            c_prime -= w
        else:
            X.append(0)

    return (int(''.join(map(str, reversed(X))), base=2).to_bytes(int(math.ceil(len(X) / 8)), byteorder='big'))


if __name__ == "__main__":
    pt = b'Hello World!'
    priv_key, pub_key = generate(len(pt))
    ct = enc(pt, pub_key)
    dt = dec(ct, priv_key)

    print(f"original:\t{pt}")
    print(f"cypher:\t\t{ct}")
    print(f"decodec:\t{dt}")
