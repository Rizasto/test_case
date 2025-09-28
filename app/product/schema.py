from typing import Optional

from pydantic import BaseModel


class ProductUpdate(BaseModel):
    id: int
    product_name: Optional[str] = None
    price: Optional[int] = None
    stashed: Optional[int] = None
    measurement: Optional[str] = None
