from pydantic import BaseModel, Field, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description='Эл.почта пользователя')
    password: str = Field(description="Пароль пользователя в чистом виде")
    nickname: str = Field(description='Никнейм пользователя')
    firstname: str = Field(description='Фамилия пользователя')
    lastname: str = Field(description='Имя пользователя')


class UserAdd(BaseModel):
    email: EmailStr = Field(description='Эл.почта пользователя')
    hashed_password: str = Field(description="Хеш пароля пользователя")
    nickname: str = Field(description='Никнейм пользователя')
    firstname: str = Field(description='Фамилия пользователя')
    lastname: str = Field(description='Имя пользователя')


class User(BaseModel):
    id: EmailStr = Field(description='id пользователя')
    email: str = Field(description='Эл.почта пользователя')
    nickname: str = Field(description='Никнейм пользователя')
    firstname: str = Field(description='Фамилия пользователя')
    lastname: str = Field(description='Имя пользователя')
