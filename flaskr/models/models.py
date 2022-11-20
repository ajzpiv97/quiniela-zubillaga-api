import re
from typing import Union

from pydantic import BaseModel, Field, validator


class RegisterBody(BaseModel):
    email: str
    name: str
    last_name: str = Field(alias='lastName')
    password: str = Field(min_length=3, max_length=20)

    # custom validation on email field
    @validator('email')
    def email_valid(cls, value: str) -> str:
        """
        Method to validate email is correct
        :param value: current email value
        :return: email value
        """
        email = value.lower()
        if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('Email provided is not valid!')
        return email


class LoginBody(BaseModel):
    email: str
    password: str = Field(min_length=3, max_length=20)


class Game(BaseModel):
    team1: str
    team2: str
    score1: Union[int, str]
    score2: Union[int, str]


class PredictionBody(BaseModel):
    try:
        predictions: list[Game]
    except Exception as e:
        print(e)