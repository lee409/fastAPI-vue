from fastapi import APIRouter, Depends, HTTPException
from redis.client import Redis
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc

from apps.system.curd.curd_dict_data import curd_dict_data
from common import deps
from common.resp import respSuccessJson

try:
    from redis.asyncio import Redis as asyncRedis
except ImportError:
    from aioredis import Redis as asyncRedis

router = APIRouter()


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
