# memory/memory_cache.py
import logging

logger = logging.getLogger(__name__)

class MemoryCache:
    """
    Класс для управления кэшированием данных памяти.
    """

    def __init__(self, max_size=None):
        """
        Инициализация кэша.
        
        :param max_size: Максимальное количество элементов в кэше (None для отсутствия ограничения).
        """
        self.cache = {}
        self.max_size = max_size
        logger.info("MemoryCache инициализирован с max_size = %s", max_size)

    def set(self, key, value):
        """
        Установить значение в кэш.

        :param key: Ключ для сохранения.
        :param value: Значение для сохранения.
        """
        try:
            if self.max_size and len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                self.cache.pop(oldest_key)
                logger.warning("Кэш достиг максимального размера. Удален старый ключ: %s", oldest_key)
            
            self.cache[key] = value
            logger.info("Добавлено в кэш: ключ = %s, значение = %s", key, value)
        except Exception as e:
            logger.error("Ошибка при добавлении в кэш: %s", e)

    def get(self, key):
        """
        Получить значение из кэша по ключу.

        :param key: Ключ для извлечения.
        :return: Значение или None, если ключ не найден.
        """
        try:
            value = self.cache.get(key)
            if value is not None:
                logger.info("Получено из кэша: ключ = %s, значение = %s", key, value)
            else:
                logger.warning("Ключ не найден в кэше: %s", key)
            return value
        except Exception as e:
            logger.error("Ошибка при получении из кэша: %s", e)
            return None

    def clear(self):
        """
        Очистить весь кэш.
        """
        try:
            self.cache.clear()
            logger.info("Кэш успешно очищен.")
        except Exception as e:
            logger.error("Ошибка при очистке кэша: %s", e)
