class FakeRedis:
    def __init__(self) -> None:
        self._db ={self._convert_to_bytes('RUR'):self._convert_to_bytes('63'),
         self._convert_to_bytes('USD'):self._convert_to_bytes('25')}
    async def get(self, key):
        return  self._db[self._convert_to_bytes(key)]
    async def set(self, key, value):
            self._db[self._convert_to_bytes(key)] = self._convert_to_bytes(value)
    async def exists(self, key):
        return  self._convert_to_bytes(key) in self._db
    async def keys(self):
        return self._db.keys()
    async def flushall(self):
        self._db.clear()
    def _convert_to_bytes(self, value):
        return bytes(value, encoding="UTF-8")