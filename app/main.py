from fastapi import Response, Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from starlette import status
from starlette.responses import JSONResponse

from .api import router as api_router
from .db import db
from .utils.utils import static_dir
# from .web import router as web_router

app = FastAPI(debug=False)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(api_router, prefix="/api")
# app.include_router(web_router)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:8080"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_accept_handler(request: Request, exc: RequestValidationError) -> Response:
	try:
		raw_errors = exc.raw_errors
		error_wrapper: ErrorWrapper = raw_errors[0]
		validation_error: ValidationError = error_wrapper.exc
		errors = validation_error.errors()
		error_type = errors[0].get("type")
		custom_detail = errors[0].get("msg", "")
		error_fields = []
		for error in errors:
			if error.get("type") == error_type:
				error_fields += error.get("loc", [])
		error_fields = ", ".join(error_fields)
		custom_detail = custom_detail + " " + error_fields
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": custom_detail}
		)
	except AttributeError:
		print(exc.raw_errors)
		return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content={"detail": "Не удалось преобразовать данные в json"}
		)


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()
