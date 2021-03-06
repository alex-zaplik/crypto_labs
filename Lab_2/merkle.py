from dataclasses import dataclass
from multiprocessing import Pool

import time
import argparse

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random
from Crypto.Util import Padding


@dataclass
class SecurityParams:
    n: int  # Bit length of keys
    N: int  # Number of puzzles


######################################################################################################
############################### Encryption and decryption with AES CBC ###############################
######################################################################################################


def encrypt(msg, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(msg)

    return ciphertext


def decrypt(sec, key):
    cipher = AES.new(key, AES.MODE_CBC, sec[:16])
    plaintext = cipher.decrypt(sec[16:])

    return plaintext


######################################################################################################
############################### Representation of Alice in the protocol ##############################
######################################################################################################


class Alice:
    def __init__(self, params: SecurityParams, K: bytes):
        self.params = params
        self.keys = []
        self.messages = []
        self.key = 0
        self.K = K

    def prepare_puzzles(self):
        """Generates a list of puzzles to be used in the protocol

        Each puzzle is a message of the form "A message prefix" + id + key where
        the 'id' is the index of a generated secure key in the key list and 'key'
        is that secure key

        Each puzzle is also encrypted with a 'params.n' bit key

        Returns:
            list: A shuffled list of encrypted puzzles
        """
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
    
    def receive_id(self, id):
        """Receives an id from Bob and sets the appropriate session key

        Args:
            id (int): The decrypted id
        """
        print(f"Alice:\tReceived a puzzle id: {id}")
        self.key = self.keys[id]

    def finalize(self):
        """Prints the status of the session after key exchange was completed
        """
        print(f"Alice:\tCommunication key: {int.from_bytes(self.key, byteorder='big')}")
    
    def send(self, msg):
        """Sends a message encrypted with the session key

        Args:
            msg (bytes): The message to be encrypted
        
        Returns:
            ct (bytes): The cyphertext
        """
        print(f"Alice:\tSending:\t{msg}")
        ct = encrypt(msg, self.key)
        print(f"\t\t\t{ct}")
        return ct
    
    def receive(self, msg):
        """Receives and decrypts a message encrypted with the session key

        Args:
            msg (bytes): The encrypted message
        """
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


######################################################################################################
############################### Representation of Bob in the protocol ################################
######################################################################################################


class Bob:
    def __init__(self, params: SecurityParams):
        self.params = params
        self.key = 0
    
    def receive_secrets(self, secrets):
        """Chooses a random puzzle and decrypts it by brute force to
        obtain the session key and its id

        Args:
            secrets (list): The list of puzzles
        
        Returns:
            id (int): The id from the decrypted puzzle
        """
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
        """Prints the status of the session after key exchange was completed
        """
        print(f"Bob:\tCommunication key: {int.from_bytes(self.key, byteorder='big')}")
    
    def send(self, msg):
        """Sends a message encrypted with the session key

        Args:
            msg (bytes): The message to be encrypted
        
        Returns:
            ct (bytes): The cyphertext
        """
        print(f"Bob:\tSending:\t{msg}")
        ct = encrypt(msg, self.key)
        print(f"\t\t\t{ct}")
        return ct
    
    def receive(self, msg):
        """Receives and decrypts a message encrypted with the session key

        Args:
            msg (bytes): The encrypted message
        """
        print(f"Bob:\tReceived:\t{msg}")
        print(f"\t\t\t{decrypt(msg, self.key)}")


######################################################################################################
########################## Time and data estimates for different parameters ##########################
######################################################################################################


# Puzzle count: 2 ** 16; Time:      2s; Message storage:   5.24 MB; Key storage:   2.09 MB
# Puzzle count: 2 ** 24; Time:     10m; Message storage:   1.34 GB; Key storage: 536.87 MB
# Puzzle count: 2 ** 32; Time:  42.67h; Message storage: 343.59 GB; Key storage: 137.44 GB
# Puzzle count: 2 ** 40; Time: 455.11d; Message storage:  87.96 TB; Key storage:  35.18 TB


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Merkle Puzzle simulation script")
    parser.add_argument("puzzle_key_size", type=int, help="The bit length of the puzzle keys")
    parser.add_argument("puzzle_count_power", type=int, help="The number of puzzles to be used, given as 2^<input>")
    args = parser.parse_args()

    # params = SecurityParams(24, 2 ** 24)
    params = SecurityParams(args.puzzle_key_size, 2 ** args.puzzle_count_power)

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
    id = bob.receive_secrets(secrets)
    crack_end = time.time()
    print()

    alice.receive_id(id)
    print()

    alice.finalize()
    bob.finalize()
    print()

    pt = Padding.pad(b'Hello Bob!', 32)
    ct = alice.send(pt)
    bob.receive(ct)
    print()

    pt = Padding.pad(b'Hello Alice!', 32)
    ct = bob.send(pt)
    alice.receive(ct)
    print()

    print(f"Puzzle memory usage:")
    print(f"\tMessage storage:\t{alice.message_memory()} bytes")
    print(f"\tKey storage:\t\t{alice.key_memory()} bytes")
    print()

    print(f"Timing:")
    print(f"\tPuzzle generation:\t{(prepare_end - prepare_start):.2f} seconds")
    print(f"\tPuzzle cracking:\t{(crack_end - crack_start):.2f} seconds")
