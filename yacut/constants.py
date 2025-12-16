"""Константы приложения."""
import string

SHORT_ID_LENGTH = 6
CUSTOM_ID_MAX_LENGTH = 16
ALLOWED_CHARS = string.ascii_letters + string.digits
RESERVED_PATHS = {'files', 'api'}

INVALID_SHORT_ID_MSG = 'Указано недопустимое имя для короткой ссылки'
SHORT_ID_EXISTS_MSG = 'Предложенный вариант короткой ссылки уже существует.'
