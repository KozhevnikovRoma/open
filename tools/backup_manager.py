import shutil
import os

class BackupManager:
    """
    Класс для управления резервным копированием и восстановлением данных.
    """

    @staticmethod
    def create_backup(source: str, backup_path: str) -> None:
        """
        Создаёт резервную копию указанной директории.

        :param source: Путь к исходной директории.
        :param backup_path: Путь для сохранения резервной копии.
        :raises ValueError: Если исходная директория не существует.
        """
        if not os.path.exists(source):
            raise ValueError(f"Source directory '{source}' does not exist.")
        
        try:
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            shutil.copytree(source, backup_path)
            print(f"Backup created at {backup_path}.")
        except Exception as e:
            print(f"Error during backup creation: {e}")
            raise

    @staticmethod
    def restore_backup(backup_path: str, destination: str) -> None:
        """
        Восстанавливает данные из резервной копии.

        :param backup_path: Путь к резервной копии.
        :param destination: Путь для восстановления данных.
        :raises ValueError: Если резервная копия не существует.
        """
        if not os.path.exists(backup_path):
            raise ValueError(f"Backup path '{backup_path}' does not exist.")
        
        try:
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(backup_path, destination)
            print(f"Backup restored from {backup_path} to {destination}.")
        except Exception as e:
            print(f"Error during backup restoration: {e}")
            raise
