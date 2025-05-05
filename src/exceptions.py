from datetime import date

from fastapi import HTTPException


class BaseExc(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class RoomNotFoundException(BaseException):
    detail = "Номер не найден"


class HotelNotFoundException(BaseException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(BaseException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(BaseException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(BaseException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BaseException):
    detail = "Пароль неверный"


class PasswordTooShortException(BaseException):
    detail = "Слишком короткий пароль"


class UserAlreadyExistsException(BaseException):
    detail = "Пользователь уже существует"


class PatchNoFieldsException(BaseException):
    detail = "Добавьте хотя бы одно поле для изменения"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже или равна дате выезда")


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(BaseHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class PasswordTooShortHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пароль не может быть короче 4 символов"


class UserAuthHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Вы уже авторизированны"


class UserNotAuthHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Вы не авторизированны"


class CreateHotelEmptyFieldsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Поля title и location не могут быть пустыми"


class PatchNoFieldsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Добавьте хотя бы одно поле для изменения"

