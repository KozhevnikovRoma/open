import os

class CleanupTool:
    """Класс для очистки файлов в указанной директории."""

    @staticmethod
    def cleanup_directory(directory_path, extensions_to_remove=None):
        """
        Удаляет файлы с заданными расширениями из указанной директории и её поддиректорий.

        :param directory_path: Путь к директории, которую нужно очистить.
        :param extensions_to_remove: Список расширений файлов для удаления (например, ['.log', '.tmp']).
                                      Если None, удаляются все файлы.
        """
        if not os.path.exists(directory_path):
            print(f"Directory does not exist: {directory_path}")
            return

        try:
            removed_files_count = 0
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if extensions_to_remove is None or file.endswith(tuple(extensions_to_remove)):
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                        removed_files_count += 1
                        print(f"Removed: {file_path}")

            print(f"Cleanup completed. Total files removed: {removed_files_count}")
        except Exception as e:
            print(f"Error during cleanup in directory {directory_path}: {e}")

if __name__ == "__main__":
    # Пример использования
    CleanupTool.cleanup_directory(
        directory_path="test_directory", 
        extensions_to_remove=[".log", ".tmp"]
    )
