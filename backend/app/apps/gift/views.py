import os

from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from utils.encrypt import get_uuid
from .models.gift import Gifts
from .schemas import *
from .curd.curd_gift import curd_gift

from common import deps, error_code

from common.resp import respSuccessJson, respErrorJson

from core import constants

router = APIRouter()


@router.get("/gift/{gift_id}", summary="获取用户信息")
async def getGift(gift_id: int, db: Session = Depends(deps.get_db)):
    gift = curd_gift.get(db, gift_id)
    if gift:
        return respSuccessJson(data=gift)
    return respErrorJson(error_code.GiftNotExist)


@router.get("/listGift", summary="获取礼物列表")
async def listGift(*,
                   db: Session = Depends(deps.get_db),
                   gift_num: int = Query(None, gt=0),
                   gift_name: str = Query(""),
                   enableflag: int = Query(None),
                   created_after_ts: int = None,
                   created_before_ts: int = None,
                   page: int = Query(1, gt=0),
                   page_size: int = Query(20, gt=0),
                   ):
    return respSuccessJson(curd_gift.search(db, gift_num=gift_num, gift_name=gift_name, enableflag=enableflag,
                                            created_after_ts=created_after_ts, created_before_ts=created_before_ts,
                                            page=page, page_size=page_size))
