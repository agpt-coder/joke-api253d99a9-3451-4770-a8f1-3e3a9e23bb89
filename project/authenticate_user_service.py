from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    """
    Response model for a successful authentication request. Includes the authentication token that should be used for subsequent requests.
    """

    token: str
    expires_in: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "a_very_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username_or_email: str) -> prisma.models.User | None:
    user = await prisma.models.User.prisma().find_first(
        where={"OR": [{"email": username_or_email}, {"id": username_or_email}]}
    )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    username_or_email: str, password: str
) -> AuthenticationResponse:
    user = await get_user(username_or_email)
    if user and await verify_password(password, user.hash):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return AuthenticationResponse(
            token=access_token, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    else:
        return AuthenticationResponse(token="", expires_in=0)
