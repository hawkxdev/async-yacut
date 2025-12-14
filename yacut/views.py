"""View-функции приложения."""
import random
import string

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.yadisk import async_upload_files


def get_unique_short_id():
    """Генерация уникального short ID."""
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=6))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница."""
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            allowed_chars = string.ascii_letters + string.digits
            is_invalid = (
                custom_id == 'files' or
                not all(c in allowed_chars for c in custom_id) or
                URLMap.query.filter_by(short=custom_id).first() is not None
            )
            if is_invalid:
                flash('Предложенный вариант короткой ссылки уже существует.')
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
def redirect_view(short_id):
    """Переадресация по короткой ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    """Страница загрузки файлов на Яндекс Диск."""
    form = FileUploadForm()
    results = None
    if form.validate_on_submit():
        uploaded = await async_upload_files(form.files.data)
        results = []
        for item in uploaded:
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
