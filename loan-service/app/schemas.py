from typing import Optional
from pydantic import BaseModel
from datetime import date

class LoanBase(BaseModel):
    book_id: int
    borrower_name: str
    loan_date: date
    return_date: Optional[date] = None

class LoanCreate(LoanBase):
    pass

class LoanUpdate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True
