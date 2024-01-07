from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=250)
