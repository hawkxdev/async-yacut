"""Загрузка файлов на Яндекс Диск."""
import asyncio

import aiohttp

from yacut import app
from yacut.settings import API_HOST, API_VERSION

DISK_TOKEN = app.config['DISK_TOKEN']

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
PUBLISH_URL = f'{API_HOST}{API_VERSION}/disk/resources/publish'
RESOURCES_URL = f'{API_HOST}{API_VERSION}/disk/resources'
PUBLIC_DOWNLOAD_URL = f'{API_HOST}{API_VERSION}/disk/public/resources/download'

AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


async def async_upload_files(images):
    """Загружает файлы параллельно."""
    if not images:
        return []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for image in images:
            tasks.append(
                asyncio.ensure_future(
                    upload_file_and_get_url(session, image)
                )
            )
        results = await asyncio.gather(*tasks)
    return results


async def upload_file_and_get_url(session, image):
    """Загружает один файл и возвращает download URL."""
    filename = image.filename
    file_data = image.read()

    params = {
        'path': f'app:/{filename}',
        'overwrite': 'true'
    }
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=params
    ) as response:
        data = await response.json()
        upload_url = data['href']

    async with session.put(upload_url, data=file_data):
        pass

    params = {'path': f'app:/{filename}'}
    async with session.put(
        PUBLISH_URL,
        headers=AUTH_HEADERS,
        params=params
    ):
        pass

    async with session.get(
        RESOURCES_URL,
        headers=AUTH_HEADERS,
        params=params
    ) as response:
        data = await response.json()
        public_url = data.get('public_url', '')

    async with session.get(
        PUBLIC_DOWNLOAD_URL,
        params={'public_key': public_url}
    ) as response:
        data = await response.json()
        download_url = data.get('href', '')

    return {
        'filename': filename,
        'download_url': download_url
    }
