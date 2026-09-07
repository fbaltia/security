from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import User, create_tables, get_session
from utils import jwt_utils, password_utils


@asynccontextmanager
async def lifespan(_: FastAPI):
	create_tables()
	yield


app = FastAPI(title='Security API', lifespan=lifespan)


class RegisterRequest(BaseModel):
	username: str = Field(min_length=3, max_length=50)
	password: str = Field(min_length=8, max_length=128)
	email: str = Field(min_length=3, max_length=254)
	role: str = Field(min_length=1, max_length=50)


class LoginRequest(BaseModel):
	username: str = Field(min_length=3, max_length=50)
	password: str = Field(min_length=1, max_length=128)


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterRequest, session: Session = Depends(get_session)):
	user = User(
		username=user_data.username,
		password_hash=password_utils.hash(user_data.password),
		email=user_data.email,
		role=user_data.role,
	)
	session.add(user)
	try:
		session.commit()
	except IntegrityError:
		session.rollback()
		raise HTTPException(status_code=409, detail='Username already exists')

	return {
		'id': user.id,
		'username': user.username,
		'email': user.email,
		'role': user.role,
	}


@app.post('/login')
def login(credentials: LoginRequest, session: Session = Depends(get_session)):
	user = session.scalar(select(User).where(User.username == credentials.username))
	if user is None or not password_utils.verify_password(credentials.password, user.password_hash):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Invalid username or password',
		)

	return {
		'access_token': jwt_utils.create_token(user.id, user.role),
		'token_type': 'bearer',
	}
