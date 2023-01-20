from fastapi import APIRouter

from .v1.users.routes import router as users_router
from .v1.clients.routes import nicknames_router, urls_router, clients_router
from .v1.orders.routes import order_files_router, orders_router


router = APIRouter()
router.include_router(users_router, prefix="/v1/users", tags=["users"])
router.include_router(nicknames_router, prefix="/v1/clients", tags=["client_nicknames"])
router.include_router(urls_router, prefix="/v1/clients", tags=["client_urls"])
router.include_router(clients_router, prefix="/v1/clients", tags=["clients"])
router.include_router(orders_router, prefix="/v1/orders", tags=["orders"])
router.include_router(order_files_router, prefix="/v1/orderFiles", tags=["order_files"])
