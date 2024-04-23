from typing import Union, List
from pydantic import BaseModel, AnyHttpUrl, conint


class GiftSchema(BaseModel):
    gift_name: str
    gift_type: int
    gift_price: int
