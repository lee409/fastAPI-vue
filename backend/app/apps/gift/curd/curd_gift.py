from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from common.curd_base import CRUDBase, CreateSchemaType
from apps.gift.models.gift import Gifts

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


# 礼物表
class CURDGift(CRUDBase):

    # def create(self, db: Session, *, obj_in: CreateSchemaType, creator_id: int = 0):
    #     obj_in_data = obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
    #     obj = self.model(**obj_in_data)
    #     db.add(obj)
    #     db.commit()
    #     db.refresh(obj)
    #     return obj

    def get(self, db: Session, _id: int, to_dict: bool = True):
        """ 通过id获取 """
        gift = db.query(self.model).filter(self.model.gift_num == _id).first()
        return gift if not to_dict else {
            'id': gift.id,
            'gift_num': gift.gift_num,
            'pkg_name': gift.pkg_name,
            'gift_name': gift.gift_name,
            'gift_pic': gift.gift_pic,
            'pic_md5': gift.pic_md5,
            'gift_type': gift.gift_type,
            'gift_vap': gift.gift_vap,
            'vap_md5': gift.vap_md5,
            'gift_level': gift.gift_level,
            'host_exp': gift.host_exp,
            'user_exp': gift.user_exp,
            'coin_price': gift.coin_price,
            'diamond_price': gift.diamond_price,
            'creator_id': gift.creator_id,
            'enableflag': gift.enableflag
        }

    def search(self, db: Session, gift_num: int = None, gift_name: str = "", enableflag: int = 0,
               created_after_ts: int = None, created_before_ts: int = None,
               page: int = 1, page_size: int = 25):
        filters = []
        if gift_num is not None:
            filters.append(self.model.gift_num == gift_num)
        if enableflag is not None:
            filters.append(self.model.enableflag == enableflag)
        if gift_name:
            filters.append(self.model.username.like(f"%{gift_name}%"))
        if created_before_ts is not None:
            filters.append(func.unix_timestamp(self.model.created_time) <= created_before_ts)
        if created_after_ts is not None:
            filters.append(func.unix_timestamp(self.model.created_time) >= created_after_ts)
        user_data, total, _, _ = curd_gift.get_multi(db, page=page, page_size=page_size, filters=filters,
                                                     order_bys=[desc(self.model.id)])
        return {'results': user_data, 'total': total}

    def insert(self, db: Session, *, obj_in, creator_id: int = 0):
        obj_in_data = obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
        obj = self.model(**obj_in_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


curd_gift = CURDGift(Gifts)
