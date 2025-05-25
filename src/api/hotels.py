from fastapi import Query, Body, Path, HTTPException, APIRouter


from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelUpdate, HotelAdd

router = APIRouter(prefix="/hotel", tags=["Отели"])


@router.get("", summary="Получаем отели с фильтром или без с пагинацией")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description='Название отеля'),
        location: str | None = Query(default=None, description='Адрес отеля'),
 ):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{id_hotel}", summary="Получение отеля по id")
async def get_hotel(id_hotel: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=id_hotel)
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return {"status": "Ok", "data": hotel}


@router.post("", summary="Добавление отеля")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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

    hotel = db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "Ok", "data": hotel}


@router.delete("/{id_hotel}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, id_hotel: int = Path(description="ID отеля для удаления")):
    await db.hotels.delete(id=id_hotel)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{id_hotel}", summary="Полное изменение данных об отеле")
async def update_hotel(id_hotel: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=id_hotel)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{id_hotel}", summary="Частичное изменение данных об отеле",
              description="Подробное описание для чего ручка. <h1>Возможно использовать теги HTML </h1> "
                          "Круто, можно поиграть с ЦВЕТОМ")
async def partial_update_hotel(id_hotel: int, hotel_data: HotelUpdate, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=id_hotel)
    await db.commit()
    return {"status": "Ok"}
