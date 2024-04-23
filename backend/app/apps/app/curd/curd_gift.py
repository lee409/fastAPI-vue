from common.curd_base import CRUDBase
from sqlalchemy import distinct, desc, asc, func
from sqlalchemy.orm import Session
from apps.permission.models.menu import Menus
from apps.permission.models.role import RoleMenu, Roles
from apps.permission.models.user import Users, UserRole
from apps.system.models import ConfigSettings
from common.curd_base import CRUDBase
from common.security import verify_password, get_password_hash
from fastapi.encoders import jsonable_encoder

class CURDGift(CRUDBase):
    def getByGiftId(self, db: Session, *, giftId: int):
        """
        通过用户名获取用户
        """
        return db.query(Gift).filter(Gift.username == username).first()

curd_user = CURDGift(Users)