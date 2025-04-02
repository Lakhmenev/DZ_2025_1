from sqlalchemy import select, insert

from src.models.hotels import HotelsOrm
from src.repo.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.where(HotelsOrm.location.icontains(location))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()
