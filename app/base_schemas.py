from pydantic import BaseModel


class CoreModel(BaseModel):
	class Config:
		orm_mode = True


class IDModelMixin(CoreModel):
	id: int
