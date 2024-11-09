import enum
import os
from dotenv import find_dotenv, load_dotenv

from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi.responses import JSONResponse
from jose import jwt, ExpiredSignatureError
from passlib.context import CryptContext

from fastapi import status

env_file = find_dotenv('.env.usuarios')
loaded = load_dotenv(env_file)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_jwt(email: str, username: str) -> str:
    data = {"email": email, "username": username}
    access_token_expires = timedelta(minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
    return create_access_token(data=data, expires_delta=access_token_expires)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get(
        "ALGORITHM") if os.environ.get("ALGORITHM") else "HS256")
    return encoded_jwt


def get_json_response(error: str, msg: str) -> JSONResponse:
    class estatusErrorsCode(enum.Enum):
        E400 = status.HTTP_400_BAD_REQUEST
        E401 = status.HTTP_401_UNAUTHORIZED
        E403 = status.HTTP_403_FORBIDDEN
        E404 = status.HTTP_404_NOT_FOUND
        E412 = status.HTTP_412_PRECONDITION_FAILED
        E422 = status.HTTP_422_UNPROCESSABLE_ENTITY

    class estatusErrorsMsg(enum.Enum):
        E400 = 'Bad Request'
        E401 = 'Unauthorized'
        E403 = 'Forbidden'
        E404 = 'Not Found'
        E412 = 'Precondition Failed'
        E422 = 'Unprocessable Entity'

    return JSONResponse(
        status_code=estatusErrorsCode[error].value,
        content={
            "statusCode": estatusErrorsCode[error].value,
            "message": msg.upper(),
            "error": estatusErrorsMsg[error].value
        },
    )
