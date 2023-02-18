import os
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from .models import User, UserInDB
from .schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_TOKEN_EXPIRES_MINUTES = int(os.environ.get("JWT_TOKEN_EXPIRES_MINUTES", 15))


class Hasher:
	@staticmethod
	def verify_password(password, hashed_password):
		return pwd_context.verify(password, hashed_password)

	@staticmethod
	def hash_password(password):
		return pwd_context.hash(password)


async def authenticate_user(username, password):
	"""Аутентифицирует пользователя

	:param str username: Имя пользователя
	:param str password: Пароль пользователя
	:return: False - если пользователь не найден или пароль не соответствует
		или информация о пользователе из бд
	:rtype: UserInDB | False
	"""
	user = await User.get_by_username(username)
	if user is None:
		return False
	if not Hasher.verify_password(password=password, hashed_password=user.password):
		return False
	return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	to_encode = data.copy()
	if expires_delta is not None:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRES_MINUTES)
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


async def get_current_user(token=Depends(oauth2_scheme)):
	"""Получает данные текущего пользователя

	:param str token: Токен пользователя
	:return: Данные о текущем авторизованном пользователе
	:rtype: UserInDB
	"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Не удалось проверить учетные данные",
		headers={"WWW-Authenticate": "Bearer"}
	)
	try:
		payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = await User.get_by_username(token_data.username)
	if user is None:
		raise credentials_exception
	return user
