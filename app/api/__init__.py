from fastapi import APIRouter

from .v1.users.routes import router as users_router
from .v1.clients.routes import nicknames_router, urls_router, clients_router


router = APIRouter()
router.include_router(users_router, prefix="/v1/users", tags=["users"])
router.include_router(nicknames_router, prefix="/v1/clients", tags=["client_nicknames"])
router.include_router(urls_router, prefix="/v1/clients", tags=["client_urls"])
router.include_router(clients_router, prefix="/v1/clients", tags=["clients"])
