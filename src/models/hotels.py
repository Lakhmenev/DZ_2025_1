from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    #  Mapped - это аннотация, которая используется для указания типа столбца в таблице базы данных и его свойства.
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]  # В данном случае нет ограничений просто тип данных указан
