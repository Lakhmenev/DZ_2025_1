from fastapi import Body, APIRouter

from src.database import async_session_maker
from src.repo.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotel", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получаем номера комнат")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получаем номер отеля по id")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавляем номер в отель")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
       "summary": "Одноместный номер",
       "value": {
           "title": "Одноместный номер",
           "description": "Одноместный номер",
           "price": 100,
           "quantity": 1,
       }
    },
    "2": {
        "summary": "Двухместный номер",
        "value": {
            "title": "Двухместный номер",
            "description": "Двухместный номер",
            "price": 200,
            "quantity": 2,
        }
    },
    })
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменяем номер отеля по id")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменяем номер отеля по id")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаляем номер отеля по id")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}