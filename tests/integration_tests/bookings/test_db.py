from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    # создание брони
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=user_id,
        user_id=room_id,
        date_from=date(year=2025, month=5, day=10),
        date_to=date(year=2025, month=5, day=20),
        price=100
    )
    booking_data = await db.bookings.add(booking_data)
    # чтение брони
    await db.bookings.get_one_or_none(id=booking_data.id)
    # обновить бронь
    await db.bookings.edit(booking_data)
    # удалить бронь
    await db.bookings.delete(id=booking_data.id)
    await db.commit()
