"""View-функции приложения."""
import random
import string

from flask import flash, render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


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
