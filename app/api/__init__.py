from fastapi import APIRouter

from .v1.users.routes import router as users_router
from .v1.clients.routes import router as clients_router


router = APIRouter()
router.include_router(users_router, prefix="/v1/users", tags=["users"])
router.include_router(clients_router, prefix="/v1/clients", tags=["clients"])

