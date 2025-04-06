from sqlalchemy import select, delete, update

from src.models.hotels import HotelsOrm
from src.repo.base import BaseRepository
from src.schemas.hotels import HotelUpdate, Hotel


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
        )
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_by_filter(
            self,
            data: HotelUpdate
    ):
        query_by_filter = select(HotelsOrm)
        if data.title:
            query_by_filter = query_by_filter.filter(HotelsOrm.title.icontains(data.title))
        if data.location:
            query_by_filter = query_by_filter.where(HotelsOrm.location.icontains(data.location))

        query_by_filter = (
            query_by_filter
        )
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(query_by_filter.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query_by_filter)
        return result.scalars().all()

    async def delete_by_filter(self, data_filter: HotelUpdate) -> None:
        query = delete(HotelsOrm)

        if data_filter.title:
            query = query.filter(HotelsOrm.title.icontains(data_filter.title))
        if data_filter.location:
            query = query.filter(HotelsOrm.location.icontains(data_filter.location))
        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(query)
        return

    async def edit_by_filter(self, data_edit: Hotel, data_filter: HotelUpdate) -> None:
        edit_stmt = update(HotelsOrm)

        if data_filter.title:
            edit_stmt = edit_stmt.filter(HotelsOrm.title.icontains(data_filter.title))
        if data_filter.location:
            edit_stmt = edit_stmt.filter(HotelsOrm.location.icontains(data_filter.location))

        edit_stmt = edit_stmt.values(**data_edit.dict())

        #  Распечатать запрос в консоль для проверки (в продакшене убираем)
        print(edit_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(edit_stmt)
        return
