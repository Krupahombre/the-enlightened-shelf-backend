from datetime import datetime, timedelta

from jose import jwt

from src.utils.config_provider import config_provider


SECRET_KEY = config_provider.get_config_value("auth", "secret_key")
ALGORITHM = config_provider.get_config_value("auth", "algorithm")
TOKEN_EXPIRE = config_provider.get_config_value("auth", "token_expire")


def create_token(user_id: int, username: str, user_role: str) -> str:
    expiration_date = datetime.now() + timedelta(minutes=int(TOKEN_EXPIRE))
    encode = {
        "sub": username,
        "id": user_id,
        "role": user_role,
        "exp": expiration_date
    }

    return jwt.encode(encode, SECRET_KEY, ALGORITHM)
