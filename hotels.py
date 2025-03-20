from fastapi import Query, Path, Body, HTTPException, APIRouter


router = APIRouter(prefix="/hotel", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "level": "4 star"},
    {"id": 2, "title": "Дубай", "level": "5 star"},
    {"id": 3, "title": "Сыктывкар", "level": "2 star"},
]


@router.get("", summary="Получаем отели с фильтром или без")
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


@router.post("", summary="Добавление отеля")
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


@router.delete("/{id_hotel}", summary="Удаление отеля")
def delete_hotel(id_hotel: int = Path(description="ID отеля для удаления")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != id_hotel]
    return {"status": "Ok"}


@router.put("/{id_hotel}", summary="Полное изменение данных об отеле")
def update_hotel(
        id_hotel: int = Path(description="ID обновляемого отеля"),
        title_hotel: str = Body(description='Название нового отеля'),
        level_hotel: str = Body(description='Уровень нового отеля')

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id_hotel:
            hotel["title"] = title_hotel
            hotel["level"] = level_hotel
            return {"status": "Ok"}
    raise HTTPException(status_code=404, detail="Отель не найден")


@router.patch("/{id_hotel}", summary="Частичное изменение данных об отеле",
              description="Подробное описание для чего ручка. <h1>Возможно использовать теги HTML </h1> "
                          "Круто, можно поиграть с ЦВЕТОМ")
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
