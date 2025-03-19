from fastapi import FastAPI, Query, Path, Body, HTTPException
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='Домашнее задание №1',
    debug=True,
    docs_url=None, redoc_url=None)  # Отключаем стандартные пути к документации

app.mount("/static", StaticFiles(directory="static"), name="static")


hotels = [
    {"id": 1, "title": "Sochi", "level": "4 star"},
    {"id": 2, "title": "Дубай", "level": "5 star"},
    {"id": 3, "title": "Сыктывкар", "level": "2 star"},
]


@app.get("/hotels")
def get_hotels(
                id_hotel: int | None = Query(default=None, description='ID отеля'),
                title_hotel: str | None = Query(default=None, description='Название отеля'),
                level_hotel: str | None = Query(default=None, description='Уровень отеля')
                ):
    hotels_ = []
    for hotel in hotels:
        if id_hotel and hotel['id'] != id_hotel:
            continue
        if title_hotel and hotel['title'] != title_hotel:
            continue
        if title_hotel and hotel['level'] != level_hotel:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title_hotel: str = Body(embed=True, description='Название нового отеля'),
        level_hotel: str = Body(embed=True, description='Уровень нового отеля')
):
    global hotels
    if len(hotels) == 0:
        new_id = 0
    else:
        new_id = hotels[-1]["id"]

    hotels.append(
        {
            "id": new_id + 1,
            "title": title_hotel,
            "level": level_hotel,
        }
    )
    return {"status": "Ok"}


@app.delete("/hotels/{id_hotel}")
def delete_hotel(id_hotel: int = Path(description="ID отеля для удаления")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id_hotel]
    return {"status": "Ok"}


@app.put("/hotels/{id_hotel}")
def update_hotel(
        id_hotel: int = Path(description="ID обновляемого отеля"),
        title_hotel: str = Body(embed=True, description='Название нового отеля'),
        level_hotel: str = Body(embed=True, description='Уровень нового отеля')

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id_hotel:
            hotel["title"] = title_hotel
            hotel["level"] = level_hotel
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")


@app.patch("/hotels/{id_hotel}")
def partial_update_hotel(
        id_hotel: int = Path(description="ID обновляемого отеля"),
        title_hotel: str | None = Body(description='Название нового отеля', default=None),
        level_hotel: str | None = Body(description='Уровень нового отеля', default=None)

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id_hotel:
            if title_hotel is not None:
                hotel["title"] = title_hotel
            if level_hotel is not None:
                hotel["level"] = level_hotel
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")


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
