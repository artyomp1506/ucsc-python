from aiohttp import web
import json


class DatabaseHandler:
    def __init__(self, storage) -> None:
        self._storage = storage
        self._validParameters = {'merge': ['0', '1']}

    async def post(self, request):
        '''
         Docs for swagger
        ---
        summary: Convert from one currency to other
        tags:
          - currencies
        requestBody:
         required: true
         content:
             application/json:
                 schema:
                  type: object
                
             
        parameters:
          - name: merge
            in:   query
            required: true
            description: If merge==0 current data will be rewrited, else added
            schema:
             type: string
             enum: [0,1]
        responses:
         '200':
           description: Result of modify database. 
           content:
             application/json:
               schema:
                 type: object
         '400':
           description: If the request is not valid
           content:
             application/json:
                schema:
                 type: object
        '''
        url_arguments = request.rel_url.query
        try:
            self.check_request_parameters_valid(url_arguments)
            data = await request.content.read()
            data = data.decode()
            json_data = json.loads(data)
            await self._storage.update(json_data, int(url_arguments['merge']))
            return web.json_response({'Status':'Complete'})
        except ValueError as error:
            return web.json_response({'Error': f'{error}'}, status=400)

    def check_request_parameters_valid(self, parametrs):
        if (len(parametrs) == len(self._validParameters)):
            for parameter in self._validParameters:
                if parameter not in parametrs:
                    raise ValueError(
                        f'There is not required parameter {parameter} in queries')
                elif parametrs[parameter] not in self._validParameters[parameter]:
                    raise ValueError(
                        f'Uncorrect value. Correct values:{[value for value in self._validParameters[parameter]]}')
            return True
        raise ValueError(
            f'Query parameters count should be {len(self._validParameters)}')
