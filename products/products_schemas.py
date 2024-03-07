from typing import Optional

from pydantic import BaseModel, Field


class ProductCreateUpdate(BaseModel):
    title: str = Field(max_length=50)
    description: Optional[str] = None
    price: int = Field(gt=0)
    category_id: int = Field(ge=1)
    quantity: int = Field(ge=0)


