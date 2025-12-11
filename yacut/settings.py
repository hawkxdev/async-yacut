"""Конфигурация приложения из переменных окружения."""
import os


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'


class Config:
    """Настройки Flask-приложения."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', default='SUP3R-S3CR3T-K3Y-F0R-MY-PR0J3CT'
    )
    DISK_TOKEN = os.getenv('DISK_TOKEN', default='')
