import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import jwt

load_dotenv()

def get_jwt_secret() -> str:
    secret = os.getenv('JWT_SECRET')
    if not secret:
        raise RuntimeError('JWT_SECRET is not configured. Add it to the environment or a .env file.')
    return secret

def create_token(id: int, role: str) -> str:
    today = datetime.now(timezone.utc)
    return jwt.encode(payload={
        'iss': 'khunly.be',
        'iat': today.timestamp(),
        'exp': timedelta(minutes=15) + today,
        'role': role,
        'sub': str(id)
    }, key=get_jwt_secret(), algorithm='HS256')

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, key=get_jwt_secret(), algorithms=['HS256'])
    except jwt.exceptions.DecodeError as e:
        raise ValueError(e) from e