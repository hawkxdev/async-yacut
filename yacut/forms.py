"""Формы приложения."""
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, ValidationError
)

from yacut.constants import (
    CUSTOM_ID_MAX_LENGTH, INVALID_SHORT_ID_MSG,
    RESERVED_PATHS, SHORT_ID_EXISTS_MSG
)
from yacut.models import URLMap


class URLForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=[
            Length(max=CUSTOM_ID_MAX_LENGTH, message=INVALID_SHORT_ID_MSG),
            Regexp(r'^[a-zA-Z0-9]*$', message=INVALID_SHORT_ID_MSG),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field: StringField) -> None:
        if (field.data in RESERVED_PATHS or
                URLMap.query.filter_by(short=field.data).first() is not None):
            raise ValidationError(SHORT_ID_EXISTS_MSG)


class FileUploadForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс Диск."""

    files = MultipleFileField('Файлы')
    submit = SubmitField('Загрузить')
