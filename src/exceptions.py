from datetime import date

from fastapi import HTTPException


class BaseExc(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseExc):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(BaseExc):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(BaseExc):
    detail = "Не сталось свободных номеров"


class IncorrectPassword(BaseExc):
    detail = "Не корректный пароль"


def check_date_to_is_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=403, detail="Дата заезда позже или ровна дате выезда")


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отеля не существует"


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номера не существует"
