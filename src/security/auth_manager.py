import os
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel

class AuthManager:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
    ALGORITHM = "HS256"

    class TokenData(BaseModel):
        username: Optional[str] = None

    async def authenticate(self, token: str) -> "UserModel":
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self.credentials_exception()
            token_data = self.TokenData(username=username)
        except JWTError:
            raise self.credentials_exception()

        user = self.get_user_from_db(username=token_data.username)
        if user is None:
            raise self.credentials_exception()
        return user

    def credentials_exception(self) -> HTTPException:
        return HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    def get_user_from_db(self, username: str) -> Optional["UserModel"]:
        # Example: query user from database
        return UserModel(username=username)

class UserModel:
    def __init__(self, username: str):
        self.username = username
