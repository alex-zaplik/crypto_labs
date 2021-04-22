from dataclasses import dataclass
from multiprocessing import Pool

import time

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random
from Crypto.Util import Padding


@dataclass
class SecurityParams:
    n: int  # Bit length of keys
    N: int  # Number of puzzles


def encrypt(msg, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(msg)

    return ciphertext


def decrypt(sec, key):
    cipher = AES.new(key, AES.MODE_CBC, sec[:16])
    plaintext = cipher.decrypt(sec[16:])

    return plaintext


class Alice:
    def __init__(self, params: SecurityParams, K: bytes):
        self.params = params
        self.keys = []
        self.messages = []
        self.key = 0
        self.K = K

    def prepare_puzzles(self):
        print("Alice:\tPreparing puzzles")

        self.keys = []
        self.messages = []

        for i in range(params.N):
            id = i.to_bytes(16, byteorder='big')
            key = encrypt(id, self.K)

            puzzle_key = random.randint(0, 2 ** params.n - 1)

            self.keys.append(key)
            self.messages.append(encrypt(b'A message prefix' + id + key, puzzle_key.to_bytes(16, byteorder='big')))
        
        print(f"Alice:\tPrepared {params.N} puzzles")

        print(f"Alice:\tShuffling puzzles")
        random.shuffle(self.messages)

        return self.messages
    
    def recieve_id(self, id):
        print(f"Alice:\tRecieved a puzzle id: {id}")
        self.key = self.keys[id]

    def finalize(self):
        print(f"Alice:\tCommunication key: {int.from_bytes(self.key, byteorder='big')}")
    
    def send(self, msg):
        print(f"Alice:\tSending:\t{msg}")
        ct = encrypt(msg, self.key)
        print(f"\t\t\t{ct}")
        return ct
    
    def recieve(self, msg):
        print(f"Alice:\tReceived:\t{msg}")
        print(f"\t\t\t{decrypt(msg, self.key)}")
    
    def message_memory(self):
        mem = 0
        for m in self.messages:
            mem += len(m)
        return mem
    
    def key_memory(self):
        mem = 0
        for k in self.keys:
            mem += len(k)
        return mem


class Bob:
    def __init__(self, params: SecurityParams):
        self.params = params
        self.key = 0
    
    def recieve_secrets(self, secrets):
        print(f"Bob:\tReceived {len(secrets)} puzzles")
        print("Bob:\tPicking a random puzzle")
        secret = secrets[random.randint(0, len(secrets) - 1)]

        print("Bob:\tBrute forcing a random puzzle")
        for i in range(2 ** params.n):
            k = i.to_bytes(16, byteorder='big')
            text = decrypt(secret, k)

            if text[:16] == b'A message prefix':
                id_bytes = text[16:32]
                id = int.from_bytes(id_bytes, byteorder='big')

                key_bytes = text[32:]
                key = int.from_bytes(key_bytes, byteorder='big')

                print(f"Bob:\tFound a solution: key={i} message={text[:16]} {id} {key}")
                self.key = key_bytes

                return id

    def finalize(self):
        print(f"Bob:\tCommunication key: {int.from_bytes(self.key, byteorder='big')}")
    
    def send(self, msg):
        print(f"Bob:\tSending:\t{msg}")
        ct = encrypt(msg, self.key)
        print(f"\t\t\t{ct}")
        return ct
    
    def recieve(self, msg):
        print(f"Bob:\tReceived:\t{msg}")
        print(f"\t\t\t{decrypt(msg, self.key)}")


# Puzzle count: 2 ** 16; Time:      2s; Message storage:   5.24 MB; Key storage:   2.09 MB
# Puzzle count: 2 ** 24; Time:     10m; Message storage:   1.34 GB; Key storage: 536.87 MB
# Puzzle count: 2 ** 32; Time:  42.67h; Message storage: 343.59 GB; Key storage: 137.44 GB
# Puzzle count: 2 ** 40; Time: 455.11d; Message storage:  87.96 TB; Key storage:  35.18 TB


if __name__ == "__main__":
    params = SecurityParams(24, 2 ** 24)

    print("Parameters:")
    print(f"\tPuzzle key size:\t{params.n} bits")
    print(f"\tNumber of puzzles:\t{params.N}")
    print()

    alice = Alice(params, get_random_bytes(16))
    bob = Bob(params)

    prepare_start = time.time()
    secrets = alice.prepare_puzzles()
    prepare_end = time.time()
    print()

    crack_start = time.time()
    id = bob.recieve_secrets(secrets)
    crack_end = time.time()
    print()

    alice.recieve_id(id)
    print()

    alice.finalize()
    bob.finalize()
    print()

    pt = Padding.pad(b'Hello Bob!', 32)
    ct = alice.send(pt)
    bob.recieve(ct)
    print()

    pt = Padding.pad(b'Hello Alice!', 32)
    ct = bob.send(pt)
    alice.recieve(ct)
    print()

    print(f"Puzzle memory usage:")
    print(f"\tMessage storage:\t{alice.message_memory()} bytes")
    print(f"\tKey storage:\t\t{alice.key_memory()} bytes")
    print()

    print(f"Timing:")
    print(f"\tPuzzle generation:\t{(prepare_end - prepare_start):.2f} seconds")
    print(f"\tPuzzle cracking:\t{(crack_end - crack_start):.2f} seconds")
