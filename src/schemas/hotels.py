from pydantic import BaseModel, Field


# Модель на добавление
class HotelAdd(BaseModel):
    title: str = Field(description='Название отеля')
    location: str = Field(description='Адрес отеля')


# Класс отеля для реализации мапинга в БД и для сериализации в json
# Модель на чтение
class Hotel(HotelAdd):
    id: int = Field(description='ID отеля')


class HotelUpdate(BaseModel):
    title: str | None = Field(None, description='Название отеля')
    location: str | None = Field(None, description='Адрес отеля')
