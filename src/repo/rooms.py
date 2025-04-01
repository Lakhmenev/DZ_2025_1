from src.models.rooms import RoomsOrm
from src.repo.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
