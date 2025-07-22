from datetime import date
from typing import Sequence

from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repo.base import BaseRepository
from src.repo.mappers.mappers import BookingDataMapper
from src.repo.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAddDTO


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
