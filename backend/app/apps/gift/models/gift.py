from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from core.config import settings

from db.base_class import Base


class Gifts(Base):
    """礼物表
    CREATE TABLE `gift` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `gift_num` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物num',
  `pkg_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '包名',
  `gift_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物名称',
  `gift_pic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物图片url',
  `pic_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物图片的MD5',
  `gift_type` int NOT NULL COMMENT '礼物类型(1: 普通礼物 2: 视频礼物)',
  `gift_vap` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物视频url',
  `vap_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '礼物视频的MD5',
  `gift_level` int NOT NULL COMMENT '礼物等级',
  `host_exp` bigint NOT NULL COMMENT '主播礼物经验',
  `user_exp` bigint DEFAULT NULL COMMENT '用户礼物经验',
  `coin_price` bigint NOT NULL COMMENT '金币单价',
  `diamond_price` bigint DEFAULT NULL COMMENT '钻石单价',
  `creator_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '创建人id',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_modifier_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '最后修改人id',
  `last_modify_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  `enableflag` int NOT NULL DEFAULT '1' COMMENT '是否启用(0: 未启用 1: 已启用)',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_gift_name` (`gift_name`) USING BTREE,
  KEY `index_price` (`coin_price`) USING BTREE,
  KEY `index_pkg_name` (`pkg_name`) USING BTREE
    ) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='礼物表'
    """
    id = Column(Integer, primary_key=True, index=True, comment="id")
    gift_num = Column(String(24), nullable=False, comment="礼物num")
    pkg_name = Column(String(255), default=None, comment="包名")
    gift_name = Column(String(255), nullable=False, comment="礼物名称")
    gift_pic = Column(String(255), nullable=False, comment="礼物图片url")
    pic_md5 = Column(String(255), nullable=False, comment="礼物图片的MD5")
    gift_type = Column(Integer, nullable=False, comment="礼物类型(1: 普通礼物 2: 视频礼物)")
    gift_vap = Column(String(255), nullable=False, comment="礼物视频url")
    vap_md5 = Column(String(255), nullable=False, comment="礼物视频的MD5")
    gift_level = Column(Integer, nullable=False, comment="礼物等级")
    host_exp = Column(Integer, nullable=False, comment="主播礼物经验")
    user_exp = Column(Integer, default=None, comment="用户礼物经验")
    coin_price = Column(Integer, nullable=False, comment="金币单价")
    diamond_price = Column(Integer, default=None, comment="钻石单价")
    creator_id = Column(String(24), default=None, comment="创建人id")
    created_time = Column(DateTime, default=None, onupdate=datetime.now, comment="创建时间")
    modifier_id = Column(String(24), default=None, comment="最后修改人id")
    modified_time = Column(DateTime, default=None, onupdate=datetime.now, comment="最后修改时间")
    is_deleted = Column(Integer, nullable=False, default=0, comment="是否删除(0: 未删除 1: 已删除)")
    enableflag = Column(Integer, nullable=False, default=1, comment="是否启用(0: 未启用 1: 已启用)")

    def __str__(self):
        return self.gift_name

    def __repr__(self):
        return self.gift_name
