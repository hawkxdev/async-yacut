"""Модели базы данных."""
from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Модель связи оригинальной и короткой ссылки."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Сериализация объекта в словарь."""
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short_id=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        """Десериализация данных из словаря."""
        setattr(self, 'original', data['url'])
        if 'custom_id' in data:
            setattr(self, 'short', data['custom_id'])
