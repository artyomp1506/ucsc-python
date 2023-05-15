from aioredis import Redis


class RedisStorage:
    def __init__(self, db: Redis) -> None:
        self._db = db

    async def get(self, value: str):
        if (await self._db.exists(value)):
            result = await self._db.get(value)
            return result.decode()
        raise ValueError(f'Database does not contain rate of {value}')

    async def get_keys(self):
        elements = []
        for key in await self._db.keys():
            elements.append(key.decode())
        return elements

    async def set(self, key: str, value: float) -> float:
        if (value==0):
            raise ValueError("Value should be positive number")
        await self._db.set(key, value)
        return value

    async def update(self, data, merge):
        if merge == 0:
           await self._db.flushall()
        for key, value in data.items():
            await self.set(key, value)
