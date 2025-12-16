"""API эндпоинты."""
from typing import Optional, Tuple

from flask import Response, jsonify, request

from yacut import app, db
from yacut.constants import (
    ALLOWED_CHARS, CUSTOM_ID_MAX_LENGTH, INVALID_SHORT_ID_MSG,
    RESERVED_PATHS, SHORT_ID_EXISTS_MSG
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


def validate_custom_id(custom_id: str) -> Optional[str]:
    """Валидация формата и уникальности."""
    if (len(custom_id) > CUSTOM_ID_MAX_LENGTH or
            not all(c in ALLOWED_CHARS for c in custom_id)):
        return INVALID_SHORT_ID_MSG
    if (custom_id in RESERVED_PATHS or
            URLMap.query.filter_by(short=custom_id).first() is not None):
        return SHORT_ID_EXISTS_MSG
    return None


@app.route('/api/id/', methods=['POST'])
def create_short_link() -> Tuple[Response, int]:
    """Создание короткой ссылки."""
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if custom_id:
        error = validate_custom_id(custom_id)
        if error:
            raise InvalidAPIUsage(error)
    url_map = URLMap()
    url_map.from_dict(data)
    if not url_map.short:
        url_map.short = get_unique_short_id()
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id: str) -> Tuple[Response, int]:
    """Получение оригинального URL."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
