from fastapi.routing import APIRouter

from .user import user_api
from .permission import permission_api
from .system import system_api
from .gift import gift_api
from .app import app_api


api_router = APIRouter()

api_router.include_router(user_api, prefix="/user")
api_router.include_router(system_api, prefix="/system")
api_router.include_router(permission_api, prefix="/permission")
api_router.include_router(gift_api, prefix="/gift")
api_router.include_router(app_api, prefix="/app")


__all__ = ['api_router']