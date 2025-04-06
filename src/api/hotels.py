from fastapi import Query, Body, Path, HTTPException, APIRouter

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repo.base import BaseRepository
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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "Ok", "data": hotel}


@router.delete("/", summary="Удаление отеля")
async def delete_hotel(id_hotel: int | None = Query(None, description="ID отеля для удаления"),
                       hotel_data: HotelUpdate = Body(None,description="Фильтры для удаления отеля(ей)"),
                       ):

    async with (async_session_maker() as session):
        if id_hotel is not None:
            result = await HotelsRepository(session).get_by_id(id_hotel)
            if result is not None:
                await HotelsRepository(session).delete_by_id(id_hotel)
                await session.commit()
                return {"status": "Ok"}
            else:
                raise HTTPException(status_code=404, detail="Отель не найден")

        if hotel_data:
            if (((hotel_data.title is None) or (hotel_data.title == ""))
                    and ((hotel_data.location is None) or (hotel_data.location == ""))):
                raise HTTPException(status_code=400, detail="Не указаны параметры для удаления отелей")
            else:
                result = await HotelsRepository(session).get_all_by_filter(hotel_data)
                if len(result) > 0:
                    await HotelsRepository(session).delete_by_filter(hotel_data)
                    await session.commit()
                    return {"status": "Ok"}
                else:
                    raise HTTPException(status_code=404, detail="Отели не найдены")


@router.put("/", summary="Полное изменение данных об отеле")
async def update_hotel(id_hotel: int | None = Query(None, description="ID отеля для обновления данных об отеле"),
                       hotel_filter: HotelUpdate | None = Body(None, description="Фильтры для изменения данных отеля(ей)"),
                       hotel_data: Hotel = Body(description="Нове данные для отеля(ей)"),
                       ):
    async with async_session_maker() as session:
        if id_hotel is not None:
            result = await HotelsRepository(session).get_by_id(id_hotel)
            if result is None:
                raise HTTPException(status_code=404, detail="Отель не найден")
            else:
                if hotel_data:
                    await HotelsRepository(session).update_by_id(id_hotel, hotel_data)
                    await session.commit()
                    return {"status": "Ok"}

        if hotel_filter:
            if (((hotel_filter.title is None) or (hotel_filter.title == ""))
                    and ((hotel_filter.location is None) or (hotel_filter.location == ""))):
                raise HTTPException(status_code=400, detail="Указаны не все параметры для изменения отеля(ей)")
            else:
                result = await HotelsRepository(session).get_all_by_filter(hotel_filter)
                if len(result) > 0:
                    await HotelsRepository(session).edit_by_filter(hotel_data, hotel_filter)
                    await session.commit()
                    return {"status": "Ok"}


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
