import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

load_dotenv()

def get_pepper() -> str:
    pepper = os.getenv('APPLICATION_PEPPER')
    if not pepper:
        raise RuntimeError('APPLICATION_PEPPER is not configured. Add it to the .env file.')
    return pepper

password_hasher = Argon2Hasher(
    memory_cost=2*16,
    parallelism=4,
    time_cost=6
)

password_context = PasswordHash([password_hasher])

def hash(plain_password: str) -> str:
    pepper = get_pepper()
    return password_context.hash(plain_password + pepper)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pepper = get_pepper()
    return password_context.verify(plain_password + pepper, hashed_password)