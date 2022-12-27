from app.base_schemas import CoreModel, IDModelMixin
from pydantic import Field, ValidationError, root_validator


class NicknameBase(CoreModel):
	nickname: str


class NicknameCreate(NicknameBase):
	pass


class NicknameUpdate(NicknameBase):
	pass


class NicknameInDB(IDModelMixin, NicknameBase):
	pass


class NicknamePublic(IDModelMixin, NicknameBase):
	pass


class UrlBase(CoreModel):
	url: str


class UrlCreate(UrlBase):
	pass


class UrlUpdate(UrlBase):
	pass


class UrlInDB(IDModelMixin, UrlBase):
	pass


class UrlPublic(IDModelMixin, UrlBase):
	pass


class ClientBase(CoreModel):
	nickname: str
	comment: str | None = None
	nicknames: list[str] | None = None
	urls: list[str] | None = None


class ClientCreate(ClientBase):
	pass


class ClientUpdate(ClientBase):
	pass


class ClientInDB(IDModelMixin, ClientBase):
	pass


class ClientPublic(IDModelMixin, ClientBase):
	pass
