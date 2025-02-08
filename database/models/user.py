from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Храним хеш пароля
    role = Column(String, default="user")  # Роль пользователя
    status = Column(String, default="active")  # Статус пользователя
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}', status='{self.status}')>"
    
    @staticmethod
    def validate_email(email):
        """Простая проверка email на валидность."""
        if "@" not in email or "." not in email.split("@")[1]:
            logger.warning(f"Invalid email format: {email}")
            raise ValueError("Invalid email format")
        return email
