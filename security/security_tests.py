import unittest
from encryption import Encryption
from access_manager import AccessManager

class TestSecurity(unittest.TestCase):
    def test_encryption(self):
        encryption = Encryption()
        original_data = 'test'
        encrypted = encryption.encrypt(original_data)
        decrypted = encryption.decrypt(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_access_manager(self):
        manager = AccessManager()
        self.assertTrue(manager.check_access('admin', 'delete'))
        self.assertFalse(manager.check_access('user', 'delete'))

if __name__ == '__main__':
    unittest.main()
