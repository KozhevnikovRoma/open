import time

class PerformanceAnalyzer:
    """Класс для анализа производительности функций."""
    
    @staticmethod
    def measure_performance(func):
        """Декоратор для измерения времени выполнения функции."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds.")
            return result
        return wrapper

# Пример использования класса
if __name__ == '__main__':
    @PerformanceAnalyzer.measure_performance
    def sample_function():
        time.sleep(2)
        print("Sample function executed.")

    sample_function()
