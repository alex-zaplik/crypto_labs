from rsa import RSA


def blind_sign(oracle: RSA, m):
    # Signed value: (m * r^e)
    # Blinded signature: (m * r^e)^d = m^d * r
    # Revealing: (m^d * r) * r_inv = m^d

    N, e = oracle.get_pubkey()

    r = oracle.random_elem()
    r_inv = pow(r, -1, N)

    # Blind the input:
    blind = m * pow(r, e, N) % N

    # Get a signature for the blinded message:
    blind_sign = oracle.sign(blind)

    # Reveal the signature
    sign = blind_sign * r_inv % N

    return sign


def blind_verify(oracle: RSA, m, s):
    return oracle.verify(m, s)


if __name__ == "__main__":
    rsa = RSA(1024)
    m = rsa.random_elem()

    test = rsa.sign(m)
    print(f"Test signature verification: {rsa.verify(m, test)}")

    blind = blind_sign(rsa, m)
    print(f"Blind signature verification: {blind_verify(rsa, m, blind)}")
