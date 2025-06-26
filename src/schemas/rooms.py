from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(description='Название номера')
    description: str = Field(None, description='Описание номера')
    price: int = Field(description='Цена номера')
    quantity: int = Field(description='Количество номеров этого типа')
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int = Field(description='id отеля')
    title: str = Field(description='Название номера')
    description: str | None = Field(None, description='Описание номера')
    price: int | None = Field(None, description='Цена номера')
    quantity: int | None = Field(None, description="Количество номеров этого типа")


class Room(RoomAdd):
    id: int = Field(description='id комнаты')

    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility] = Field()


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None, description='Название номера')
    description: str | None = Field(None, description='Описание номера')
    price: int | None = Field(None, description='Цена номера')
    quantity: int | None = Field(None, description='Количество номеров этого типа')
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None, description='id отеля')
    title: str | None = Field(None, description='Название номера')
    description: str | None = Field(None, description='Описание номера')
    price: int | None = Field(None, description='Цена номера')
    quantity: int | None = Field(None, description='Количество номеров этого типа')
