from fastapi import APIRouter, Body

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repo.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "user1",
                "value": {
                    "email": "email1@gmail.com",
                    "password": "pass1",
                    "nickname": "nick1",
                    "lastname": "last1",
                    "firstname": "first1"
                }
            },
            "2": {
                "summary": "user2",
                "value": {
                    "email": "email2@gmail.com",
                    "password": "pass2",
                    "nickname": "nick2",
                    "lastname": "last2",
                    "firstname": "first2"

                }
            },
        })
):
    hashed_password = pwd_context.hash(data.password)
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
