from sqlalchemy import select, delete, update

from src.repo.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.where(HotelsOrm.location.icontains(location))

        query = (
            query
        )
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]



