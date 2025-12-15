"""View-функции приложения."""
import random
from typing import Optional

from flask import abort, flash, redirect, render_template
from werkzeug.wrappers import Response

from yacut import app, db
from yacut.constants import (
    ALLOWED_CHARS, CUSTOM_ID_MAX_LENGTH, RESERVED_PATHS, SHORT_ID_LENGTH
)
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.yadisk import async_upload_files


def get_unique_short_id() -> str:
    """Генерация уникального short ID."""
    while True:
        short_id = ''.join(random.choices(ALLOWED_CHARS, k=SHORT_ID_LENGTH))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id


def validate_custom_id(custom_id: str) -> Optional[str]:
    """Проверяет custom_id, возвращает ошибку или None если валидный."""
    if len(custom_id) > CUSTOM_ID_MAX_LENGTH:
        return 'Указано недопустимое имя для короткой ссылки'
    if not all(c in ALLOWED_CHARS for c in custom_id):
        return 'Указано недопустимое имя для короткой ссылки'
    if custom_id in RESERVED_PATHS:
        return 'Предложенный вариант короткой ссылки уже существует.'
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        return 'Предложенный вариант короткой ссылки уже существует.'
    return None


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    """Главная страница."""
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            error = validate_custom_id(custom_id)
            if error:
                flash(error)
                return render_template('index.html', form=form)
            short = custom_id
        else:
            short = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('index.html', form=form, url_map=url_map)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id: str) -> Response:
    """Переадресация по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
async def files_view() -> str:
    """Страница загрузки файлов на Яндекс Диск."""
    form = FileUploadForm()
    results = None
    if form.validate_on_submit():
        uploaded = await async_upload_files(form.files.data)
        results = []
        for item in uploaded:
            if not item.get('download_url'):
                results.append({
                    'filename': item['filename'],
                    'short': None,
                    'error': item.get('error', 'Ошибка загрузки')
                })
                continue
            short = get_unique_short_id()
            url_map = URLMap(
                original=item['download_url'],
                short=short
            )
            db.session.add(url_map)
            results.append({
                'filename': item['filename'],
                'short': short
            })
        db.session.commit()
    return render_template('files.html', form=form, results=results)
