"""Обработчики ошибок."""
from typing import Dict, Optional, Tuple

from flask import Response, jsonify, render_template

from yacut import app, db


class InvalidAPIUsage(Exception):
    """Исключение для ошибок API."""

    status_code = 400

    def __init__(
        self, message: str, status_code: Optional[int] = None
    ) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> Dict[str, str]:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> Tuple[Response, int]:
    """Обработчик ошибок API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error: Exception) -> Tuple[str, int]:
    """Обработчик ошибки 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error: Exception) -> Tuple[str, int]:
    """Обработчик ошибки 500."""
    db.session.rollback()
    return render_template('500.html'), 500
