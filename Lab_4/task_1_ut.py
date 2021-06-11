import unittest
import parameterized

from Crypto.Cipher import AES
from libs import crypto_libs, utils


TESTED_MODES = [(AES.MODE_CBC, ), (AES.MODE_ECB, ), (AES.MODE_OFB, )]


class CryptoLibsTests(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.message = b'test data'
        self.secret = utils.bytes_from_hex("6701a2bc291276a6e56701a2bc291276")


    def encrypt_in_mode(self, mode):
        return crypto_libs.encrypt(self.message, self.secret, mode)


    def decrypt_in_mode(self, encryption, mode):
        return crypto_libs.decrypt(encryption, self.secret,  mode)


    @parameterized.parameterized.expand(TESTED_MODES)
    def test_encryption_modes(self, tested_mode):
        encrypted_data = self.encrypt_in_mode(tested_mode)
        decrypted_data = self.decrypt_in_mode(encrypted_data, tested_mode)
        self.assertEqual(self.message, decrypted_data)


if __name__ == '__main__':
    unittest.main()
