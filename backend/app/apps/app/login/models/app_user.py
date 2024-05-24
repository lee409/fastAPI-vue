from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.config import settings

from db.base_class import Base


class AppUser(Base):
    """移动客户端用户表
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
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `last_modifier_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '最后修改人id',
  `last_modify_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
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
    id = Column(Integer, primary_key=True, index=True, comment="id")
    user_id = Column(String(24), nullable=False, comment="用户id")
    role_type = Column(Integer, nullable=False, comment="角色类型")
    platform = Column(Integer, nullable=False, comment="平台")
    uuid = Column(String(255), nullable=False, comment="平台唯一标识id")
    email = Column(String(255), default=None, comment="电子邮件")
    device_id = Column(String(255), nullable=False, comment="设备id")
    token = Column(String(255), nullable=False, comment="app登录token")
    rong_cloud_token = Column(String(255), default=None, comment="融云token")
    last_login_time = Column(DateTime, nullable=False, comment="上次登录时间")
    coin_balance = Column(Integer, nullable=False, default=0, comment="金币钱包")
    audit_status = Column(Integer, nullable=False, comment="审核状态")
    ban_status = Column(Integer, nullable=False, default=0, comment="封禁状态(0: 未被封禁 1: 已封禁)")
    ban_begin_time = Column(DateTime, default=None, comment="封禁开始时间")
    ban_duration = Column(Integer, default=0, comment="封禁时长(秒)")
    creator_id = Column(String(24), default=None, comment="创建人id")
    created_time = Column(DateTime, default=None, comment="创建时间")
    modifier_id = Column(String(24), default=None, comment="最后修改人id")
    modified_time = Column(DateTime, default=None, onupdate=datetime.now, comment="最后修改时间")
    enableflag = Column(Integer, nullable=False, default=1, comment="是否启用(0: 未启用 1: 已启用)")

    def __str__(self):
        return self.user_id

    def __repr__(self):
        return self.nick_name
