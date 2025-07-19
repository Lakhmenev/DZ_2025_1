from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path
from fastapi.staticfiles import StaticFiles

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # При выключении/перезапуске приложения
    await redis_manager.close()


app = FastAPI(
    lifespan=lifespan,
    title='Проект ОТЕЛИ',
    debug=True,
    docs_url=None,  # Отключаем стандартные пути к документации
    redoc_url=None,  # Отключаем стандартные пути к документации
)

app.include_router(router_auth)  # Подключаем ручки по авторизации
app.include_router(router_hotels)  # Подключаем ручки по отелям
app.include_router(router_rooms)  # Подключаем ручки по комнатам
app.include_router(router_bookings)  # Подключаем ручки по бронированиям
app.include_router(router_facilities)  # Подключаем ручки по удобствам
app.include_router(router_images)  # Подключаем ручки по изображениям отелей

app.mount("/static", StaticFiles(directory="src/static"), name="static")


#  Переводим swagger документацию на статические файлы
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


#  Переводим redoc документацию на статические файлы
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1', port=8111, log_level="info", reload=True)
