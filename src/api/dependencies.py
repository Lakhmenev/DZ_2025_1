from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    # пагинация с ограничением страница не может быть <1 ge=1
    page: Annotated[int | None, Query(default=1, description='Номер страницы', ge=1)]
    # пагинация с ограничением, что значение должно быть от 1 и до 5
    per_page: Annotated[int | None, Query(default=None, description='Количество отелей на странице', ge=1, le=50)]


PaginationDep = Annotated[PaginationParams, Depends()]
