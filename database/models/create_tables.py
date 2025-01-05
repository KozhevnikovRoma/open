from database.database_manager import DatabaseManager

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()
    print("Таблицы успешно созданы!")
