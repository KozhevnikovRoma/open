import logging
import numpy as np
from memory.memory_manager import MemoryManager  # Добавленный импорт

class VectorManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.memory_manager = MemoryManager(storage_file="vector_storage.bin")

    def add_vector(self, key, vector):
        """Добавляет вектор в память"""
        if not isinstance(vector, (list, np.ndarray)) or not all(isinstance(x, (int, float)) for x in vector):
            self.logger.error(f"Неверный формат вектора: {vector}")
            raise ValueError("Vector must be a list or numpy array of numbers")
        self.logger.debug(f"Добавление вектора с ключом '{key}': {vector}")
        try:
            self.memory_manager.set_memory(key, vector)
            self.logger.info(f"Вектор успешно добавлен с ключом '{key}'.")
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении вектора с ключом '{key}': {e}")

    def calculate_similarity(self, key1, key2):
        """Вычисляет схожесть между двумя векторами"""
        self.logger.debug(f"Извлечение векторов для ключей '{key1}' и '{key2}'")
        try:
            vector1 = self.memory_manager.get_memory(key1)
            vector2 = self.memory_manager.get_memory(key2)
        except Exception as e:
            self.logger.error(f"Ошибка при извлечении векторов: {e}")
            return 0

        if not vector1 or not vector2:
            self.logger.warning(f"Один или оба вектора не найдены или пустые для ключей '{key1}' и '{key2}'!")
            return 0

        try:
            dot_product = np.dot(vector1, vector2)
            norm_a = np.linalg.norm(vector1)
            norm_b = np.linalg.norm(vector2)
            self.logger.debug(f"Скалярное произведение: {dot_product}, нормы: {norm_a}, {norm_b}")
        except Exception as e:
            self.logger.error(f"Ошибка при вычислении схожести: {e}")
            return 0

        if norm_a == 0 or norm_b == 0:
            self.logger.warning(f"Один из векторов имеет нулевую норму для ключей '{key1}' и '{key2}'!")
            return 0

        similarity = dot_product / (norm_a * norm_b)
        self.logger.debug(f"Вычисленная схожесть: {similarity}")
        return similarity
