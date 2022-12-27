from fastapi import APIRouter
from .users.routes import router as users_router
from .dashboard.routes import router as dashboard_router


router = APIRouter()
router.include_router(users_router, tags=["users-web"])
router.include_router(dashboard_router, tags=["dashboard-web"])
