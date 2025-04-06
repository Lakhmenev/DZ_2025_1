from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_by_id(self, id: int):
        query = select(self.model).filter_by(id=id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def delete_by_id(self, id: int) -> None:
        delete_stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(delete_stmt)
        return

    async def update_by_id(self, id: int, data: BaseModel):
        edit_stmt = update(self.model).where(self.model.id == id).values(**data.model_dump()).returning(self.model)
        print(edit_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(edit_stmt)
        pass
        return result.scalars().one()
