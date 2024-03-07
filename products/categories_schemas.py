from pydantic import BaseModel, Field


class CategoryCreateUpdate(BaseModel):
    title: str = Field(max_length=50)
