from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    #  Mapped - это аннотация, которая используется для указания типа столбца в таблице базы данных и его свойства.
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    nickname: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
