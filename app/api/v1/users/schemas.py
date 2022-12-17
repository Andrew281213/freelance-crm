from app.base_schemas import CoreModel, IDModelMixin
from pydantic import Field, ValidationError, validator, root_validator

PASSWORD_MIN_LENGTH = 5
PASSWORD_MAX_LENGTH = 64


class UserBase(CoreModel):
	username: str


class UserCreate(UserBase):
	password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)


class UserUpdate(UserBase):
	new_password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH)
	new_password_repeat: str

	@root_validator
	def check_passwords(cls, values):
		pw1, pw2 = values.get("new_password"), values.get("new_password_repeat")
		if pw1 is None or pw2 is None or pw1 != pw2:
			raise ValidationError()


class UserInDB(IDModelMixin, UserBase):
	password: str


class UserPublic(IDModelMixin, UserBase):
	pass
