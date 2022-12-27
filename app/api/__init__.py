from fastapi import APIRouter

from .v1.users.routes import router as users_router


router = APIRouter()
router.include_router(users_router, prefix="/v1/users", tags=["users"])
