from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIDDep
from src.database import async_session_maker
from src.repo.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(
        response: Response,
        data: UserLogin = Body(openapi_examples={
            "1": {
                "summary": "user1",
                "value": {
                    "email": "email1@gmail.com",
                    "password": "pass1",
                }
            },
            "2": {
                "summary": "user2",
                "value": {
                    "email": "email2@gmail.com",
                    "password": "pass2",
                }
            },
        }),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        # if user is None:
        #     raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        # if not AuthService().verify_password(data.password, user.hashed_password):
        #     raise HTTPException(status_code=401, detail="Неверный пароль")
        #   Чтобы не делать подсказку, что именно пароль или email не верный, можно сделать так:
        if (user is None) or (not AuthService().verify_password(data.password, user.hashed_password)):
            raise HTTPException(status_code=401, detail="Неверный пароль или email")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "user1",
                "value": {
                    "email": "email1@gmail.com",
                    "password": "pass1",
                    "nickname": "nick1",
                    "firstname": "firstname1",
                    "lastname": "lastname1"
                }
            },
            "2": {
                "summary": "user2",
                "value": {
                    "email": "email2@gmail.com",
                    "password": "pass2",
                    "nickname": "nick2",
                    "firstname": "firstname2",
                    "lastname": "lastname3"
                }
            },
        })
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email,
                            hashed_password=hashed_password,
                            nickname=data.nickname,
                            lastname=data.lastname,
                            firstname=data.firstname
                            )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.get("/me")
async def get_me(
        user_id: UserIDDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.delete("/logout")
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
