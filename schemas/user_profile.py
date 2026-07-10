from pydantic import BaseModel,Field

class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str

class UserProfileCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=7, max_length=20)