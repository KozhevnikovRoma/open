import unittest
from memory.memory_manager import MemoryManager
from memory.vector_manager import VectorManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager(storage_file="test_memory_storage.json")

    def test_save_and_retrieve_memory(self):
        key = "test_key"
        value = "test_value"
        self.memory_manager.set_memory(key, value)

        result = self.memory_manager.get_memory(key)
        self.assertEqual(result, value, "Failed to save and retrieve memory")

    def tearDown(self):
        import os
        if os.path.exists("test_memory_storage.json"):
            os.remove("test_memory_storage.json")


class TestVectorManager(unittest.TestCase):
    def setUp(self):
        print("Setting up VectorManager")
        self.vector_manager = VectorManager()
        print("VectorManager initialized")

    def test_vector_addition_and_similarity(self):
        print("Starting test_vector_addition_and_similarity")
        key1 = "vector1"
        key2 = "vector2"
        vector1 = [1, 2, 3]
        vector2 = [1, 2, 3]
        print("Adding vectors")
        self.vector_manager.add_vector(key1, vector1)
        self.vector_manager.add_vector(key2, vector2)

        print("Calculating similarity")
        similarity = self.vector_manager.calculate_similarity(key1, key2)
        print(f"Similarity calculated: {similarity}")
        self.assertAlmostEqual(similarity, 1.0, places=2, msg="Failed vector similarity calculation")


if __name__ == "__main__":
    unittest.main()
