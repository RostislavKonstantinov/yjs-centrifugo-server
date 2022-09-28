import typing as t

import logging
import httpx
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger(__name__)


async def send_message(message: t.Dict[str, t.Any]) -> bool:
    async with httpx.AsyncClient() as client:
        client.headers.update({'Authorization': 'apikey cbf46e80-3e00-4642-8f3a-369b8707304d'})
        data = {
            'method': 'publish',
            'params': {
                'channel': 'signal',
                'data': message
            }
        }
        response: httpx.Response = await client.post(
            url='http://centrifugal:8000/api',
            json=data,
        )
        logger.info(f'message: {message}, response: {response.json()}')
        try:
            response.raise_for_status()
            return True
        except Exception:
            return False


@app.post('/api/message/')
async def read_message(message: t.Dict[str, t.Any]) -> t.Dict[str, bool]:
    status = await send_message(message)
    return {'status': status}
