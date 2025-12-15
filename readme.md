# YaCut

Сервис сокращения ссылок с возможностью загрузки файлов на Яндекс Диск.

## Автор

Sergey Sokolkin — [GitHub](https://github.com/hawkxdev/)

## Tech Stack

- [Python 3.11](https://www.python.org/)
- [Flask 3.0](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy 3.1](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate 4.0](https://flask-migrate.readthedocs.io/)
- [Flask-WTF 1.2](https://flask-wtf.readthedocs.io/)
- [aiohttp 3.10](https://docs.aiohttp.org/)

## Локальное развертывание

### 1. Клонирование репозитория

```bash
git clone git@github.com:hawkxdev/yacut.git
cd yacut
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
```

Linux/macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
source venv/Scripts/activate
```

### 3. Установка зависимостей

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key-here
DISK_TOKEN=your-yandex-disk-oauth-token
YADISK_API_HOST=https://cloud-api.yandex.net/
```

### 5. Применение миграций

```bash
flask db upgrade
```

### 6. Запуск сервера

```bash
flask run
```

Приложение доступно по адресу: http://127.0.0.1:5000/
