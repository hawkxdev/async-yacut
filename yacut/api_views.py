"""API эндпоинты."""
from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создание короткой ссылки."""
    data = request.get_json()
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
        return jsonify({'message': 'Указанный id не найден'}), 404
    return jsonify({'url': url_map.original}), 200
