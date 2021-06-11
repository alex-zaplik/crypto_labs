from rsa import RSA
from random import randint
from decimal import *
from multiprocessing import Pool

import time


DEBUG = 0


def debug(level, *args, end='\n'):
    if DEBUG >= level:
        print(" ".join(map(str,args)), end=end)


def generate_sets(oracle: RSA, bit, sample_count):
    set_1 = [] # No extra reduction
    set_2 = [] # Extra reduction

    N, e = oracle.get_pubkey()

    power = oracle.state_at_bit(bit)
    prev_power = 2 if bit < 2 else oracle.state_at_bit(bit - 1)

    max_val_1 = int(Decimal(N) ** Decimal(1 / power))
    max_val_2 = int(Decimal(N) ** Decimal(1 / prev_power))

    if 2 >= max_val_1 or max_val_1 >= max_val_2:
        return [], [], max_val_1, max_val_2

    try_count = sample_count * 2

    while len(set_1) < sample_count:
        num = randint(2, max_val_1)
        if not oracle.will_reduce(num, bit):
            set_1.append(num)
        
        try_count -= 1
        if try_count <= 0:
            break

    try_count = sample_count * 2

    while len(set_2) < sample_count:
        num = randint(max_val_1, max_val_2)
        if oracle.will_reduce(num, bit):
            set_2.append(num)
        
        try_count -= 1
        if try_count <= 0:
            break
    
    return set_1, set_2, max_val_1, max_val_2


def get_time_of_set(oracle: RSA, data_set):
    
    reductions = 0
    start = time.time()
    for m in data_set:
        _, t = oracle.dec(m)
        reductions += t
    end = time.time()
    
    return reductions, end - start


def run_attack(oracle: RSA, sample_count, bit_count):
    prev_bits_reduct = [1]
    prev_bits_time = [1]

    redu_acc = 0
    time_acc = 0

    for l in range(1, bit_count):
        debug(1, f"Generating for bit {l}...")

        res = generate_sets(oracle, l, sample_count)
        set_1 = res[0]
        set_2 = res[1]

        debug(1, "Simulating...")
        reduct_1, time_1 = get_time_of_set(oracle, set_1)
        reduct_2, time_2 = get_time_of_set(oracle, set_2)

        # Reduction based guess
        if reduct_1 < reduct_2:
            prev_bits_reduct.append(1)
        else:
            prev_bits_reduct.append(0)

        compare_str = ">=" if reduct_1 >= reduct_2 else "<"
        debug(1, "Redu:")
        debug(1, f"\t{reduct_1 / 1000} {compare_str} {reduct_2 / 1000}", end="\n\t")
        if DEBUG > 0 or l == bit_count - 1:
            redu_acc = oracle.compare_exponents(prev_bits_reduct)

        # Time based guess
        if time_1 * 1.008 < time_2:
            prev_bits_time.append(1)
        else:
            prev_bits_time.append(0)

        compare_str = ">=" if time_1 * 1.008 >= time_2 else "<"
        debug(1, "Time:")
        debug(1, f"\t{time_1} * 1.008 {compare_str} {time_2}", end="\n\t")
        if DEBUG > 0 or l == bit_count - 1:
            time_acc = oracle.compare_exponents(prev_bits_time)

        if DEBUG > 0 or l == bit_count - 1:
            print()

    return redu_acc, time_acc


if __name__ == "__main__":
    redu_acc = []
    time_acc = []

    for _ in range(16):
        debug(1, "Generating RSA oracle...")
        rsa = RSA(128)
        r, t = run_attack(rsa, 7500, 5)
        redu_acc.append(r)
        time_acc.append(t)
    
    print(f"Reduction accuracy: {(sum(redu_acc) / len(redu_acc)) * 100}%")
    print(f"Time accuracy: {(sum(time_acc) / len(time_acc)) * 100}%")
