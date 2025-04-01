from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(description='Название отеля')
    location: str = Field(description="Адрес отеля")


class HotelUpdate(BaseModel):
    title: str | None = Field(description='Название отеля', default=None)
    location: str | None = Field(description='Адрес отеля', default=None)
