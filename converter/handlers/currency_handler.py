from aiohttp import web
from converter.converter import Converter

class CurrencyHandler:
    def __init__(self, storage):
        self._storage = storage
        self._validParameters = ['from', 'to', 'amount']

    async def get(self, request: web.Request) -> web.Response:
        """
        Docs for swagger
        ---
        summary: Convert from one currency to other
        tags:
          - currencies
        parameters:
          - name: from
            in: path
            required: true
            description: The old currency
            schema:
             type: string
          - name: to
            in: path
            required: true
            description: The new currency
            schema:
             type: string
          - name: amount
            in: path
            required: true
            description: amount
            schema:
             type: string
        responses:
         '200':
           description: Result with currency of new rate  
           content:
             application/json:
               schema:
                 type: object
         '400':
           description: If the request is not valid or there is no such currency as it
           content:
             application/json:
                schema:
                 type: object
        """ 
        params = request.rel_url.query
        self._validate(params)
        from_value = params['from']
        to_value = params['to']
        amount_value = params['amount']
        try:
            from_rate = float(await self._storage.get(from_value))
            to_rate = float(await self._storage.get(to_value))
            converter = Converter()
            result = converter.convert(from_rate, to_rate, amount_value)
            response = {'Converted': result}
            return web.json_response(response)
        except Exception as error:
         return web.json_response({'Error': f'{error}'}, status=400)

    def check_request_parameters_valid(self, parametrs):
        if (len(parametrs) == len(self._validParameters)):
           for parameter in self._validParameters:
                if parameter not in parametrs:
                    raise ValueError(
                        f'There is not required parameter {parameter} in queries')
           return True
        raise ValueError(f'Query parameters count should be {len(self._validParameters)}')
        
    def _validate(self, parameters):
        try:
            self.check_request_parameters_valid(parameters)
        except ValueError as error:
            return web.Response(text=f"error {error}", status=400)
