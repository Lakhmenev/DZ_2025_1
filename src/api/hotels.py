from fastapi import Query, Body, Path, HTTPException, APIRouter

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelUpdate, Hotel

router = APIRouter(prefix="/hotel", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "level": "4 star"},
    {"id": 2, "title": "Дубай", "level": "5 star"},
    {"id": 3, "title": "Мальдивы", "level": "5 star"},
    {"id": 4, "title": "Геленджик", "level": "3 star"},
    {"id": 5, "title": "Москва", "level": "5 star"},
    {"id": 6, "title": "Казань", "level": "4 star"},
    {"id": 7, "title": "Санкт-Петербург", "level": "3 star"},
    {"id": 8, "title": "Сыктывкар", "level": "2 star"},
]


@router.get("", summary="Получаем отели с фильтром или без")
def get_hotels(
                pagination: PaginationDep,
                id_hotel: int | None = Query(default=None, description='ID отеля'),
                title_hotel: str | None = Query(default=None, description='Название отеля'),
                level_hotel: str | None = Query(default=None, description='Уровень отеля'),
                ):
    hotels_ = []
    for hotel in hotels:
        if id_hotel and hotel['id'] != id_hotel:
            continue
        if title_hotel and hotel['title'] != title_hotel:
            continue
        if level_hotel and hotel['level'] != level_hotel:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[(pagination.page-1) * pagination.per_page:][:pagination.per_page]  # Срез для пагинации
    return hotels_


@router.post("", summary="Добавление отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
       "summary": "Сочи",
       "value": {
           "title": "Sochi",
           "location": "ул. Славы 4",
       }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Дубай",
            "location": "ул. Пушкина 5",
        }
    },
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #  Распечатать запрос в консоль для проверки
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "Ok"}


@router.delete("/{id_hotel}", summary="Удаление отеля")
def delete_hotel(id_hotel: int = Path(description="ID отеля для удаления")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id_hotel]
    return {"status": "Ok"}


@router.put("/{id_hotel}", summary="Полное изменение данных об отеле")
def update_hotel(id_hotel: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id_hotel:
            hotel["title"] = hotel_data.title
            hotel["level"] = hotel_data.level
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")


@router.patch("/{id_hotel}", summary="Частичное изменение данных об отеле",
              description="Подробное описание для чего ручка. <h1>Возможно использовать теги HTML </h1> "
                          "Круто, можно поиграть с ЦВЕТОМ")
def partial_update_hotel(id_hotel: int, hotel_date: HotelUpdate):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id_hotel:
            if hotel_date.title is not None:
                hotel["title"] = hotel_date.title
            if hotel_date.level is not None:
                hotel["level"] = hotel_date.level
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")
