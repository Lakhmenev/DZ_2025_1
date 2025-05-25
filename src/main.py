from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
# from src.config import settings


# print(f'{settings.DB_URL=}')


app = FastAPI(
    title='Проект ОТЕЛИ',
    debug=True,
    docs_url=None, redoc_url=None)  # Отключаем стандартные пути к документации

app.include_router(router_auth)  # Подключаем ручки по авторизации
app.include_router(router_hotels)  # Подключаем ручки по отелям
app.include_router(router_rooms)  # Подключаем ручки по комнатам
app.include_router(router_bookings) # Подключаем ручки по бронированиям

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
