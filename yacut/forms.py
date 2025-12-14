"""Формы приложения."""
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
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


class FileUploadForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс Диск."""

    files = MultipleFileField('Файлы')
    submit = SubmitField('Загрузить')
