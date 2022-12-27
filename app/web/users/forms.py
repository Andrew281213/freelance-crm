from fastapi import Request


class LoginForm:
	def __init__(self, request: Request):
		self.request = request
		self.errors = []
		self.username: str | None = None
		self.password: str | None = None

	async def load_data(self):
		form = await self.request.form()
		self.username = form.get("username")
		self.password = form.get("password")

	def is_valid(self):
		if self.username is None:
			self.errors.append("Введите логин")
		if self.password is None or len(self.password) < 5 or len(self.password) > 64:
			self.errors.append("Пароль должен быть от 5 до 64 символов")
		if len(self.errors) == 0:
			return True
		return False
