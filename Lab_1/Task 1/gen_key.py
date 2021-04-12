#!/usr/bin/env python3
# Script by Aleksander Lasecki

import argparse
from Crypto.PublicKey import RSA

def egcd(a, b):
    x, y = 0, 1
    u, v = 1, 0
    
    steps = 0

    # print("    \\[\n\ta = {},\\ b = {},\\ x = {},\\ y = {},\\ u = {},\\ v = {}\n    \\]".format(a, b, x, y, u, v))

    while a != 0:
        steps += 1

        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        
        b, a = a, r
        x, y = u, v
        u, v = m, n

        # print("    \\[\n\ta = {},\\ b = {},\\ x = {},\\ y = {},\\ u = {},\\ v = {}\n    \\]".format(a, b, x, y, u, v))

    gcd = b
    return gcd, x, y, steps

# key = RSA.importKey(open('files/publickey.pem').read())
# p = 1524938362073628791222322453937223798227099080053904149
# q = 1385409854850246784644682622624349784560468558795524903

# private_key = RSA.construct((
#     key.n,
#     key.e,
#     pow(key.e, -1, (p - 1) * (q - 1)),
#     p,
#     q
# ))

# key_text = private_key.exportKey()
# print(key_text)


parser = argparse.ArgumentParser(description="Generate private key files from numeric data (p, q, e)")
parser.add_argument('p', type=int, help="Larger prime factor")
parser.add_argument('q', type=int, help="Smaller prime factor")
parser.add_argument('e', type=int, help="Public exponent")
args = parser.parse_args()

p = args.p
q = args.q
e = args.e

private_key = RSA.construct((
    p * q,
    e,
    pow(e, -1, (p - 1) * (q - 1)),
    p,
    q
))

key_text = private_key.exportKey()
print(key_text.decode('utf-8'))
