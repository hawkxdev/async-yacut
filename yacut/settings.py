"""Конфигурация приложения из переменных окружения."""
import os


API_HOST = os.getenv('YADISK_API_HOST', 'https://cloud-api.yandex.net/')


class Config:
    """Настройки Flask-приложения."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISK_TOKEN = os.getenv('DISK_TOKEN', default='')
