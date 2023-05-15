from aiohttp import web
from aioredis import from_url
from converter.models.redis_storage import RedisStorage
from converter.handlers.currency_handler import CurrencyHandler
from converter.handlers.currency_list_handler import CurrencyListHandler
from converter.handlers.database_handler import DatabaseHandler
from converter.converter import Converter
from aiohttp_swagger3 import SwaggerDocs, SwaggerInfo, SwaggerUiSettings
def get_app(storage):
    
    currency_handler = CurrencyHandler(storage)
    currency_list_handler = CurrencyListHandler(storage)
    database_handler = DatabaseHandler(storage)
    app = web.Application()
    app.router.add_get('/convert', currency_handler.get, allow_head=False)
    app.router.add_get('/currencies', currency_list_handler.get)
    app.router.add_post('/database', database_handler.post)
    swagger = SwaggerDocs(app,
    swagger_ui_settings=SwaggerUiSettings(path="/api"),
    info=SwaggerInfo(title="Currency converter", version="1.0.0"))
    swagger.add_routes([
        web.get("/currencies", currency_list_handler.get, allow_head=False),
        web.get("/convert?from={from}&to={to}&amount={amount}", currency_handler.get, allow_head=False),
        web.post("/database", database_handler.post)
    ])
    return app
