from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Book(Base):  # Apenas a definição básica necessária para a chave estrangeira
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrower_name = Column(String, index=True)
    loan_date = Column(Date)
    return_date = Column(Date, nullable=True)

    book = relationship("Book")
