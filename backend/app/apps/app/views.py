from fastapi import APIRouter, Depends, Query
from fastapi.params import Form
from redis.client import Redis
from sqlalchemy.orm import Session

from apps.app.login.curd.curd_app_user import curd_app_user
from common import deps
from common.resp import respSuccessJson
import time
import datetime

from utils.token_manager import verify_token, validate_signature, generate_token

try:
    from redis.asyncio import Redis as asyncRedis
except ImportError:
    from aioredis import Redis as asyncRedis

router = APIRouter()


# 创建一个移动端可以请求的接口
# 移动端请求的接口分为两类，一类是需要登录的，一类是不需要登录的
# 不需要登录的接口，可以直接访问，不需要token
# 需要登录的接口，需要token，token是通过登录接口获取的
# 登录接口是一个特殊的接口，不需要token，但是需要用户名和密码
# 登录接口返回token，token是一个字符串，后续需要在请求头中带上token
# token的有效期是1天
# token过期后，需要重新登录获取token
# token是一个加密的字符串，用于验证用户的身份

# 1. 登录接口; 查询 t_app_user表 是否存在该用户，如果不存在则创建一个新用户
@router.post("/login", summary="登录接口")
async def login(*,
                db: Session = Depends(deps.get_db),
                redis: Redis = Depends(deps.get_redis),
                client_ip: str = Depends(deps.get_ipaddress),
                oauthType: str = Form(...),
                deviceId: str = Form(...)):
    # 查询数据库中t_app_user表是否存在该用户
    user = curd_app_user.get_user_by_device_id(db, deviceId, to_dict=False)
    if not user:
        # 如果不存在则在t_app_user表创建一个新用户
        # `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
        # `user_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户id',
        #  `role_type` int NOT NULL COMMENT '角色类型',
        #  `platform` int NOT NULL COMMENT '平台',
        #  `uuid` BINARY(16) NOT NULL COMMENT '平台唯一标识id',
        #  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电子邮件',
        #  `device_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '设备id',
        #  `token` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'app登录token',
        #  `rong_cloud_token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '',
        #  `last_login_time` datetime NOT NULL COMMENT '上次登录时间',
        #  `coin_balance` bigint NOT NULL DEFAULT '0' COMMENT '金币钱包',
        #  `audit_status` int NOT NULL COMMENT '审核状态',
        #  `ban_status` int NOT NULL DEFAULT '0' COMMENT '封禁状态(0: 未被封禁 1: 已封禁)',
        #  `ban_begin_time` datetime DEFAULT NULL COMMENT '封禁开始时间',
        #  `ban_duration` bigint DEFAULT '0' COMMENT '封禁时长(秒)',
        #  `creator_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '创建人id',
        #  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
        #  `modifier_id` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '最后修改人id',
        #  `modified_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
        #  `enableflag` int NOT NULL DEFAULT '1' COMMENT '是否启用(0: 未启用 1: 已启用)',
        timestamp = int(time.time())

        # 将时间戳转换为DateTime对象
        datetime_obj = datetime.datetime.fromtimestamp(timestamp)
        userId = curd_app_user.generate_user_id()
        print("随机user_id:", userId)
        user_data = {
            "user_id": userId,
            "role_type": 1,
            "platform": 1,
            "email": "",
            "device_id": deviceId,
            "uuid": curd_app_user.generate_uuid(),
            "token": generate_token(userId),
            "rong_cloud_token": "",
            "last_login_time": datetime_obj,
            "coin_balance": 0,
            "audit_status": 1,
            "ban_status": 0,
            "ban_duration": 0,
            "creator_id": "",
            "created_time": datetime_obj,
            "modifier_id": "",
            "modified_time": datetime_obj,
            "enableflag": 1
        }
        print(user_data)
        user = curd_app_user.create(db, user_data, 0)
    else:
        # 更新用户的最后登录时间
        user.last_login_time = datetime.datetime.now()
        if user.token is None:
            user.token = generate_token(user.user_id)
        else:
            # 判断Token是否失效
            if verify_token(user.user_id, user.token) is False:
                user.token = generate_token(user.user_id)

        db.commit()
    return respSuccessJson(data={"token": user.token})


# 3. 获取用户信息接口
@router.get("/getUserInfo", summary="获取用户信息接口",
            dependencies=[Depends(validate_signature)])
async def getUserInfo(*,
                      db: Session = Depends(deps.get_db),
                      redis: Redis = Depends(deps.get_redis),
                      client_ip: str = Depends(deps.get_ipaddress),
                      userId: str = Query("userId")):
    user = curd_app_user.get(db, userId, to_dict=True)
    return respSuccessJson(data=user)

# 4. 修改用户信息接口
# 5. 获取用户列表接口
# 6. 获取用户详情接口
# 7. 删除用户接口
# 8. 获取礼物列表接口
# 9. 获取礼物详情接口

# @router.post("/sendGift", summary="幸运礼物jackpot")
# async def sendGift(*,
#                    db: Session = Depends(deps.get_db),
#                    redis: Redis = Depends(deps.get_redis),
#                    client_ip: str = Depends(deps.get_ipaddress),
#                    type: str = Depends(deps.user_perm(["perm:user:post"])),
#                    type: device = Depends(deps.user_perm(["perm:user:post"])),
#                    ):
#     db.getGift()
#     return respSuccessJson()
