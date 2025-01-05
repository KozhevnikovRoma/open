
import unittest
from security.access_manager import AccessManager

class TestSecurity(unittest.TestCase):
    def test_access_roles(self):
        manager = AccessManager()
        self.assertTrue(manager.has_access("admin", "write"))

if __name__ == '__main__':
    unittest.main()
