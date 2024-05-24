from typing import Union, List
from pydantic import BaseModel, AnyHttpUrl, conint


class AppUserSchema(BaseModel):
    deviceId: str


class RegisterUserInfoSchema(BaseModel):
    userId: str
    deviceId: str
    gender: str
    nickname: str = ""
    avatar: str = ""
