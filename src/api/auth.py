from fastapi import APIRouter, Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (IncorrectPasswordHTTPException, IncorrectPasswordException,
                            EmailNotRegisteredHTTPException, EmailNotRegisteredException,
                            UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException,
                            PasswordTooShortException, PasswordTooShortHTTPException, UserAuthHTTPException,
                            UserNotAuthHTTPException)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except PasswordTooShortException:
        raise PasswordTooShortHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        request: Request,
        db: DBDep,
):
    if request.cookies.get("access_token"):
        raise UserAuthHTTPException
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="👩‍💻 Мои профиль")
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
        request: Request
):
    if not request.cookies.get("access_token"):
        raise UserNotAuthHTTPException
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response, request: Request):
    if not request.cookies.get("access_token"):
        raise UserNotAuthHTTPException
    response.delete_cookie("access_token")
    return {"status": "OK"}
