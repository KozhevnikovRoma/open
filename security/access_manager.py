import os
import json

class AccessManager:
    def __init__(self, roles_file="roles.json"):
        """Инициализация менеджера доступа"""
        # Создаем абсолютный путь к файлу ролей
        roles_file = os.path.join(os.path.dirname(__file__), roles_file)
        with open(roles_file, "r") as f:
            self.roles = json.load(f)

    def get_permissions(self, role):
        """Получение разрешений для заданной роли"""
        return self.roles.get(role, [])

    def has_access(self, role, permission):
        """
        Проверка наличия разрешения у роли.
        :param role: Роль пользователя (например, "admin").
        :param permission: Проверяемое разрешение (например, "write").
        :return: True, если разрешение есть, иначе False.
        """
        permissions = self.get_permissions(role)
        return permission in permissions

