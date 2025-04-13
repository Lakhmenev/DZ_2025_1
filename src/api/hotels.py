from fastapi import Query, Body, Path, HTTPException, APIRouter


from src.api.dependencies import PaginationDep
from src.database import async_session_maker
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


@router.delete("/{id_hotel}", summary="Удаление отеля")
async def delete_hotel(id_hotel: int = Path(description="ID отеля для удаления")):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=id_hotel)
        await session.commit()
    return {"status": "Ok"}


@router.put("/{id_hotel}", summary="Полное изменение данных об отеле")
async def update_hotel(id_hotel: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=id_hotel)
        await session.commit()
    return {"status": "Ok"}


@router.patch("/{id_hotel}", summary="Частичное изменение данных об отеле",
              description="Подробное описание для чего ручка. <h1>Возможно использовать теги HTML </h1> "
                          "Круто, можно поиграть с ЦВЕТОМ")
async def partial_update_hotel(id_hotel: int, hotel_data: HotelUpdate):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=id_hotel)
        await session.commit()
    return {"status": "Ok"}
