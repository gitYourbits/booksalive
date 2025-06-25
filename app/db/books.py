from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text)

class BookSummary(Base):
    __tablename__ = "book_summaries"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    summary = Column(Text)

# Async CRUD stubs (implement later)
async def get_books(db: AsyncSession):
    pass

async def get_book(db: AsyncSession, book_id: int):
    pass

async def create_book(db: AsyncSession, book_data):
    pass

async def update_book(db: AsyncSession, book_id: int, book_data):
    pass

async def get_summary(db: AsyncSession, book_id: int):
    pass

async def update_summary(db: AsyncSession, book_id: int, summary):
    pass 