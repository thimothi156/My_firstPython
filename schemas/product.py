from pydantic import BaseModel,Field
from schemas.category import CategoryData

class ProductCreate(BaseModel):
    name:str = Field(min_length = 3, max_length = 100)
    price: int = Field(gt = 0)
    stock: int = Field(ge = 0)
    category_id: int

class ProductResponse(BaseModel):
     id: int
     name:str
     price: int
     stock: int
     category: CategoryData | None