"""API эндпоинты."""
import string

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id

ALLOWED_CHARS = string.ascii_letters + string.digits


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if custom_id:
        if (len(custom_id) > 16
                or not all(c in ALLOWED_CHARS for c in custom_id)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    if not url_map.short:
        url_map.short = get_unique_short_id()
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение оригинального URL."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
