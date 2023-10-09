from datetime import datetime, timedelta
from typing import Dict, Optional, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette import status

from src.utils.config_provider import config_provider

SECRET_KEY = config_provider.get_config_value("auth", "secret_key")
ALGORITHM = config_provider.get_config_value("auth", "algorithm")
TOKEN_EXPIRE = config_provider.get_config_value("auth", "token_expire")

bearer = HTTPBearer(scheme_name="Bearer")


def create_token(user_id: int, username: str, user_role: str) -> str:
    expiration_date = datetime.now() + timedelta(minutes=int(TOKEN_EXPIRE))
    encode = {
        "sub": username,
        "id": user_id,
        "role": user_role,
        "exp": expiration_date
    }

    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


def check_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    return validate_token(credentials.credentials)


def validate_token(token: str) -> Optional[Dict[str, str]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate user with provided token."
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate user with provided token."
        )


token_dependency = Annotated[dict, Depends(check_token)]
