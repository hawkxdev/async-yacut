"""Константы приложения."""
import string

SHORT_ID_LENGTH = 6
CUSTOM_ID_MAX_LENGTH = 16
ALLOWED_CHARS = string.ascii_letters + string.digits
RESERVED_PATHS = {'files', 'api'}
