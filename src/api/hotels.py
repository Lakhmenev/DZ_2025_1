from fastapi import Query, Body, Path, HTTPException, APIRouter

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repo.hotels import HotelsRepository
from src.schemas.hotels import HotelUpdate, Hotel

router = APIRouter(prefix="/hotel", tags=["Отели"])


@router.get("", summary="Получаем отели с фильтром или без")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description='Название отеля'),
        location: str | None = Query(default=None, description='Адрес отеля'),
 ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", summary="Добавление отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
       "summary": "Сочи",
       "value": {
           "title": "Sochi",
           "location": "Сочи, ул. Славы 4",
       }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Stars",
            "location": "Дубай, ул. Шейха 5",
        }
    },
})
):
    async with async_session_maker() as session:
        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
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
            hotel["location"] = hotel_data.level
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
                hotel["location"] = hotel_date.level
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")
