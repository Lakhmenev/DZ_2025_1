from sqlalchemy import select, func
from datetime import date

from src.models.rooms import RoomsOrm
from src.repo.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repo.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    # async def get_all(
    #         self,
    #         title,
    #         location,
    #         limit,
    #         offset,
    # ) -> list[Hotel]:
    #     query = select(HotelsOrm)
    #     if title:
    #         query = query.filter(HotelsOrm.title.icontains(title))
    #     if location:
    #         query = query.where(HotelsOrm.location.icontains(location))
    #
    #     query = (
    #         query
    #     )
    #     #  Распечатать запрос в консоль для проверки (в продакшене убираем)
    #     print(query.compile(compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #     return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title,
            location,
            limit,
            offset
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))

        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
