from pydantic import BaseModel, EmailStr
from schemas.post import PostResponse
from schemas.user_profile import UserProfileResponse


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    profile: UserProfileResponse | None
    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    user: list[UserResponse]
    post: list[PostResponse]
        