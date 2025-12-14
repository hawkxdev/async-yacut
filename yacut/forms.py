"""Формы приложения."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=[Length(max=16), Optional()]
    )
    submit = SubmitField('Создать')
