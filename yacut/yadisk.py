"""Загрузка файлов на Яндекс Диск."""
import asyncio
from typing import Dict, List

import aiohttp
from aiohttp import ClientSession
from werkzeug.datastructures import FileStorage

from yacut import app
from yacut.settings import API_HOST

DISK_TOKEN = app.config['DISK_TOKEN']

REQUEST_UPLOAD_URL = f'{API_HOST}v1/disk/resources/upload'
DOWNLOAD_URL = f'{API_HOST}v1/disk/resources/download'

AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


async def async_upload_files(
    images: List[FileStorage]
) -> List[Dict[str, str]]:
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


async def upload_file_and_get_url(
    session: ClientSession, image: FileStorage
) -> Dict[str, str]:
    """Загружает один файл и возвращает download URL."""
    filename = image.filename
    filedata = image.read()
    filepath = f'app:/{filename}'

    try:
        async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params={'path': filepath, 'overwrite': 'true'}
        ) as response:
            data = await response.json()
            upload_url = data['href']

        async with session.put(upload_url, data=filedata):
            pass

        async with session.get(
            DOWNLOAD_URL,
            headers=AUTH_HEADERS,
            params={'path': filepath}
        ) as response:
            data = await response.json()
            download_url = data.get('href', '')

        return {
            'filename': filename,
            'download_url': download_url
        }
    except (aiohttp.ClientError, KeyError) as e:
        return {
            'filename': filename,
            'download_url': '',
            'error': str(e)
        }
