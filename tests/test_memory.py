import unittest
from fastapi.testclient import TestClient
from server.server import app  # Подключаем приложение FastAPI

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        # Инициализация менеджера памяти
        from memory.memory_manager import MemoryManager
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
        from memory.vector_manager import VectorManager
        self.vector_manager = VectorManager()

    def test_vector_addition_and_similarity(self):
        key1 = "vector1"
        key2 = "vector2"
        vector1 = [1, 2, 3]
        vector2 = [1, 2, 3]

        self.vector_manager.add_vector(key1, vector1)
        self.vector_manager.add_vector(key2, vector2)

        similarity = self.vector_manager.calculate_similarity(key1, key2)
        self.assertAlmostEqual(similarity, 1.0, places=2, msg="Failed vector similarity calculation")


class TestOpenAIAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)  # Создание клиента для тестирования FastAPI

    def test_generate_text(self):
        # Тестирование генерации текста с использованием OpenAI
        response = self.client.post("/api/memory/generate-text/", json={"prompt": "Hello, AI!", "max_tokens": 50})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("generated_text", data)
        self.assertIsInstance(data["generated_text"], str)
        self.assertGreater(len(data["generated_text"]), 0, "Generated text should not be empty")

if __name__ == "__main__":
    unittest.main()
