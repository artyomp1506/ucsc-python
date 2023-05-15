from aiohttp import web


class CurrencyListHandler:

    def __init__(self, storage) -> None:
        self._storage = storage

    async def get(self, request):
        '''
        Docs for swagger
        ---
        summary: Convert from one currency to other
        tags:
         - currencies
        responses:
         '200':
              description: Show all avaliable currencies or empty response, when no avaliable.
              content:
                 application/json:
                     schema:
                         type: object
        '''
        currencies = await self._storage.get_keys()
        rates = {}
        for currency in currencies:
            rate = float(await self._storage.get(currency))
            rates[currency] = rate
        return web.json_response({'rates': rates})
