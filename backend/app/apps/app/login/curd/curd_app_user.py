import random

from fastapi.encoders import jsonable_encoder
from gunicorn.config import User
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from common.curd_base import CRUDBase, CreateSchemaType
from apps.app.login.models.app_user import AppUser
import uuid

"""用户表
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `user_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
  `role_type` int NOT NULL COMMENT '角色类型',
  `platform` int NOT NULL COMMENT '平台',
  `uuid` BINARY(16) NOT NULL COMMENT '平台唯一标识id',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电子邮件',
  `device_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备id',
  `token` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'app登录token',
  `rong_cloud_token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '融云token',
  `last_login_time` datetime NOT NULL COMMENT '上次登录时间',
  `coin_balance` bigint NOT NULL DEFAULT '0' COMMENT '金币钱包',
  `audit_status` int NOT NULL COMMENT '审核状态',
  `ban_status` int NOT NULL DEFAULT '0' COMMENT '封禁状态(0: 未被封禁 1: 已封禁)',
  `ban_begin_time` datetime DEFAULT NULL COMMENT '封禁开始时间',
  `ban_duration` bigint DEFAULT '0' COMMENT '封禁时长(秒)',
  `creator_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '创建人id',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `modifier_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '最后修改人id',
  `modified_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  `enableflag` int NOT NULL DEFAULT '1' COMMENT '是否启用(0: 未启用 1: 已启用)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `index_role_type` (`role_type`),
  KEY `index_platform` (`platform`),
  KEY `index_last_login_time` (`last_login_time`),
  KEY `index_creator_id` (`creator_id`),
  KEY `index_last_modifier_id` (`last_modifier_id`),
  KEY `index_user_num` (`user_id`),
  KEY `index_device_id` (`device_id`),
  KEY `index_uuid` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=2521 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户表';
"""


# 移动客户端用户表
class CURDAppUser(CRUDBase):

    # def create(self, db: Session, *, obj_in: CreateSchemaType, creator_id: int = 0):
    #     obj_in_data = obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
    #     obj = self.model(**obj_in_data)
    #     db.add(obj)
    #     db.commit()
    #     db.refresh(obj)
    #     return obj

    @staticmethod
    def generate_user_id():
        # 生成一个8~10位的随机数字
        user_id = str(random.randint(1e7, 1e10 - 1))
        return user_id

    @staticmethod
    def generate_uuid():
        return str("123")

    # 通过user_id获取用户
    def get(self, db: Session, _id: int, to_dict: bool = True):
        user = db.query(self.model).filter(self.model.user_id == _id).first()
        return user if not to_dict else {
            'user_id': user.user_id,
            'role_type': user.role_type,
            'platform': user.platform,
            'email': user.email,
            'rong_cloud_token': user.rong_cloud_token,
            'coin_balance': user.coin_balance,
            'audit_status': user.audit_status,
            'ban_status': user.ban_status,
            'ban_duration': user.ban_duration,
            'enableflag': user.enableflag
        }

    # 通过device_id获取用户
    def get_user_by_device_id(self, db: Session, device_id: str, to_dict: bool = True):
        user = db.query(self.model).filter(self.model.device_id == device_id).first()
        return user if not to_dict else {
            'id': user.id,
            'user_id': user.user_id,
            'role_type': user.role_type,
            'platform': user.platform,
            'uuid': user.uuid,
            'email': user.email,
            'device_id': user.device_id,
            'token': user.token,
            'rong_cloud_token': user.rong_cloud_token,
            'last_login_time': user.last_login_time,
            'coin_balance': user.coin_balance,
            'audit_status': user.audit_status,
            'ban_status': user.ban_status,
            'ban_begin_time': user.ban_begin_time,
            'ban_duration': user.ban_duration,
            'creator_id': user.creator_id,
            'created_time': user.created_time,
            'modifier_id': user.modifier_id,
            'modified_time': user.modified_time,
            'enableflag': user.enableflag
        }

    # 创建用户
    def create(self, db: Session, obj_in, creator_id: int = 0):
        obj_in_data = obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
        obj = self.model(**obj_in_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


curd_app_user = CURDAppUser(AppUser)
