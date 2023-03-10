from pydantic import Field

from app.base_schemas import CoreModel, IDModelMixin


# TODO: добавить проверку на длину ника


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
	fio: str
	comment: str = ""
	nicknames: list[NicknamePublic] = Field(default_factory=list)
	urls: list[UrlPublic] = Field(default_factory=list)


class ClientCreate(ClientBase):
	nicknames: list[int] = Field(default_factory=list)
	urls: list[int] = Field(default_factory=list)


class ClientUpdate(ClientBase):
	pass


class ClientInDB(IDModelMixin, ClientBase):
	pass


class ClientPublic(IDModelMixin, ClientBase):
	pass
