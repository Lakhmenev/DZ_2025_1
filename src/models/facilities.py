from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    #  Mapped - это аннотация, которая используется для указания типа столбца в таблице базы данных и его свойства.
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'

    #  Mapped - это аннотация, которая используется для указания типа столбца в таблице базы данных и его свойства.
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id'))
