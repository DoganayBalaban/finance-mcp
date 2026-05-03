from pydantic import BaseModel
from datetime import date
from enum import Enum

class TransactionType(Enum):
    INCOME="income"
    EXPENSE="expense"

class Transaction(BaseModel):
    date:date
    description:str
    category:str
    amount:float
    type:TransactionType

class Budget(BaseModel):
    category:str
    monthly_limit:float
    year:int
    month:int
