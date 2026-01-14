from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from .constants import EMAIL_REGEX, VALID_TYPES

class TransactionData(BaseModel):
    id:str = Field(...,min_length=1, max_length=15, alias="transaction_id")
    type:str = Field(...,min_length=1, max_length=20)
    counterparty:Optional[str] = None
    amount:float = Field(..., gt=0, description="amount can't be neither 0 nor negative")
    tags: list[str] = Field(default_factory=list)
    timestamp: str = Field(..., alias="transaction_timestamp")

    @field_validator("tags", mode="before")
    def check_tags(cls, v: Any) -> Any:
        return [] if v is None else v

    @field_validator("type")
    def check_type(self, v:str) -> str:
        if v not in VALID_TYPES:
            raise ValueError("type must be one of {}".format(VALID_TYPES))
        return v

class ProductData(BaseModel):
    id:str = Field(...,min_length=1, max_length=15, alias="product_id")
    name:str = Field(...,min_length=1, max_length=50)

class UserData(BaseModel):
    id:str = Field(...,min_length=1, max_length=15, alias="user_id")
    username:str = Field(...,min_length=1, max_length=50, alias="name")
    email:str = Field(...,min_length=1, max_length=50, alias="email_address", pattern=EMAIL_REGEX)
    age:Optional[int] = 0

    @field_validator("email", mode='after')
    def lowercase_email_address(self, v:str) -> str:
        return v.lower()

