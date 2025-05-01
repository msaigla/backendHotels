class BaseExc(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseExc):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BaseExc):
    detail = "Не сталось свободных номеров"


class DateFromLaterThanDateTo(BaseExc):
    detail = "Дата заезда позже или ровна дате выезда"


class UserExistsEmail(BaseExc):
    detail = "Пользователь с таким email уже существует"


class IncorrectPassword(BaseExc):
    detail = "Не корректный пароль"
