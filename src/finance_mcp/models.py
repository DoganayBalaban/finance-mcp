import re
from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum

class TransactionType(Enum):
    INCOME="income"
    EXPENSE="expense"

class Transaction(BaseModel):
    date:date
    description:str = Field(min_length=1, max_length=500)
    category:str = Field(min_length=1, max_length=100)
    amount:float = Field(gt=0)
    type:TransactionType

    @field_validator('description', 'category')
    @classmethod
    def strip_control_chars(cls, v: str) -> str:
        return re.sub(r'[\x00-\x1f\x7f]', ' ', v).strip()

class Budget(BaseModel):
    category: str = Field(min_length=1, max_length=100)
    monthly_limit: float
    year: int
    month: int

    @field_validator('category')
    @classmethod
    def strip_control_chars(cls, v: str) -> str:
        return re.sub(r'[\x00-\x1f\x7f]', ' ', v).strip()
