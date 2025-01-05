from sqlalchemy import Column, Integer, String, DateTime, Index
from database.database_manager import Base
from datetime import datetime

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(500), nullable=False)  # Ограничение на длину сообщения
    level = Column(String(50), nullable=False)  # Уровень логирования, например INFO, ERROR
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_logs_timestamp", "timestamp"),  # Индекс для оптимизации по времени
    )

    def __repr__(self):
        # Сокращение сообщения для удобного вывода
        short_message = (self.message[:75] + "...") if len(self.message) > 75 else self.message
        return f"<Log(id={self.id}, level={self.level}, message={short_message}, timestamp={self.timestamp})>"
