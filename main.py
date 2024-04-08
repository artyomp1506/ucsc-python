import asyncio
from aiohttp import web
import json
from aioredis import from_url
from converter.models.redis_storage import RedisStorage
from helpers import get_app

async def init():
    db = await from_url("redis://redis:6379")
    storage = RedisStorage(db)
    app = get_app(storage)
    
    app['storage'] = {}
    return app

web.run_app(init())
print("111")
