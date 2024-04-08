from tests.fake_redis import FakeRedis
from converter.models.redis_storage import RedisStorage
import unittest



class StorageTestCase(unittest.IsolatedAsyncioTestCase):
    def get_storage(self):
        return RedisStorage(FakeRedis())
    async def test_get_value_when_currency_is_valid(self):
        storage = self.get_storage()
        result = await storage.get('RUR')
        self.assertEqual(result, '63')
    async def test_fail_when_key_is_invalid(self):
        storage = self.get_storage()
        with self.assertRaises(ValueError):
            result = await storage.get("abc")
    async def test_rewrite_when_update_with_no_merge(self):
        rates = {'EUR':'80'}
        storage = self.get_storage()
        await storage.update(rates, 0)
        keys = await storage.get_keys()
        self.assertListEqual(keys, ['EUR'])
        value = await storage.get('EUR')
        self.assertEqual(value, '80')



if __name__ == "__main__":
    unittest.main("test_storage")
