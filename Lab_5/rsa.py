import math
import random
from sympy import randprime


#########################################################################
################# A comprehensive implementation of RSA #################
#########################################################################


class RSA:
    
    def __init__(self, n):
        self.p = randprime(2 ** n, 2 ** (n + 1))
        self.q = randprime(2 ** n, 2 ** (n + 1))
        self.N = self.p * self.q

        m = (self.p - 1) * (self.q - 1)
        self.e = 2 ** 16 + 1
        self.d = pow(self.e, -1, m)

        self.d_bin = list(map(int, "{0:b}".format(self.d)))
        self.e_bin = list(map(int, "{0:b}".format(self.e)))


    def random_elem(self, a=0 , b=0):
        if a == 0 and b == 0:
            r = random.randrange(2, self.N)
            while math.gcd(r, self.N) != 1:
                r = random.randrange(2, self.N)
            return r
        else:
            r = random.randrange(a, b)
            while math.gcd(r, self.N) != 1:
                r = random.randrange(a, b)
            return r


    def __mod_reduce(self, a):
        r = 0
        if a >= self.N:
            a = a % self.N
            r = 1
        return a, r
    

    def __fast_pow(self, c, bits, n=0):
        bits_work = bits[1:] if n == 0 else bits[1:n]

        reductions = 0
        x = c

        for b in bits_work:
            x, r = self.__mod_reduce(x ** 2)
            reductions += r

            if b == 1:
                x, r = self.__mod_reduce(x * c)
                reductions += r
        
        if n == 0:
            return x, reductions
        else:
            x, r = self.__mod_reduce(x ** 2)
            reductions += r

            x, r = self.__mod_reduce(x * c)
            reductions += r

            return x, reductions
    

    def fast_pow(self, c, bit):
        reductions = 0
        x = c

        index = 1
        reduced = False

        for b in self.d_bin[1:]:
            x, r = self.__mod_reduce(x ** 2)
            reductions += r

            if index == bit and x * c >= self.N:
                reduced = True

            if b == 1:
                x, r = self.__mod_reduce(x * c)
                reductions += r
            
            index += 1
        
        return x, reductions, reduced
    

    def state_at_bit(self, bit):
        p = 1

        for b in self.d_bin[1:bit]:
            p *= 2
            if b == 1:
                p += 1
        
        # Assume that the last bit is a one
        return p * 2 + 1


    def will_reduce(self, c, bit):
        reductions = 0
        x = c

        for b in self.d_bin[1:bit]:
            x, r = self.__mod_reduce(x ** 2)

            if b == 1:
                x, r = self.__mod_reduce(x * c)
        
        x, r = self.__mod_reduce(x ** 2)
        x, r = self.__mod_reduce(x * c)
        return r > 0


    def get_pubkey(self):
        return self.N, self.e


    def enc(self, m):
        return pow(m, self.e, self.N)
    

    def dec(self, c, blind=False):
        if not blind:
            return self.__fast_pow(c, self.d_bin)
        else:
            rand = self.random_elem()
            rand_inv = pow(rand, -1, self.N)

            cr1, r1 = self.__fast_pow(rand, self.e_bin)
            cr2, r2 = self.__mod_reduce(c * cr1)

            # cr2 = (m ** e) * (rand ** e) = (m * rand) ** e
            # (cr2 ** d) * rand_inv = (m * rand) * rand_inv = m

            m1, r3 = self.__fast_pow(cr2, self.d_bin)
            m2, r4 = self.__mod_reduce(m1 * rand_inv)

            return m2, r1 + r2 + r3 + r4
    

    def sign(self, m):
        return pow(m, self.d, self.N)
    

    def verify(self, m, s):
        return m == pow(s, self.e, self.N)
    

    def dec_partial(self, c, bit):
        return self.__fast_pow(c, self.d_bin, n=bit)

    
    def compare_exponents(self, d_bin):
        OK = '\033[92m'
        NO = '\033[91m'
        EN = '\033[0m'

        correct = 0
        print("[", end="")

        for i in range(len(d_bin)):
            b = d_bin[i]

            if b == self.d_bin[i]:
                print(OK, end="")
                correct += 1
            else:
                print(NO, end="")
            
            print(str(b) + EN, end="")

            if i < len(d_bin) - 1:
                print(", ", end="")
            
        print(f"] -> {(correct / len(d_bin)) * 100}%")

        return correct / len(d_bin)


    def test(self):
        print(f"RSA(N = {self.N}, d = {self.d}, e = {self.e})")
        print()

        m = self.random_elem()
        print(f"m = {m}")

        c_test = pow(m, self.e, self.N)
        d_test = pow(c_test, self.d, self.N)

        print(f"Correct: c = {c_test}, d = {d_test}")
        print()

        c = self.enc(m)

        correct = "Correct" if c_test == c else "Incorrect"
        print(f"c = {c} - {correct}")
        print()

        d, r = self.dec(c)

        correct = "Correct" if d_test == d else "Incorrect"
        print(f"d = {d} - {correct}")

        d_blind, r = self.dec(c, blind=True)

        correct = "Correct" if d_test == d_blind else "Incorrect"
        print(f"d_blind = {d_blind} - {correct}")
    
    
    def test_fast(self):
        count = 1000

        reductions = 0
        for _ in range(count):
            y = self.random_elem(2, math.floor(self.N ** (1 / 3)))
            x, r = self.__fast_pow(y, self.d_bin, 1)
            reductions += r
        print(reductions / count)

        reductions = 0
        for _ in range(count):
            y = self.random_elem(math.floor(self.N ** (1 / 3)), math.floor(self.N ** (1 / 2)))
            x, r = self.__fast_pow(y, self.d_bin, 1)
            reductions += r
        print(reductions / count)


if __name__ == "__main__":
    rsa = RSA(256)
    rsa.test()
    print()
    rsa.test_fast()
    
