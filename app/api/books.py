from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book, BookCreate, BookUpdate, BookSummary
from app.db.books import get_books as db_get_books, get_book as db_get_book, create_book as db_create_book, update_book as db_update_book, get_summary as db_get_summary, update_summary as db_update_summary
from app.db import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await db_get_books(db)

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await db_get_book(db, book_id)

@router.post("/", response_model=Book)
async def put_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await db_create_book(db, book)

@router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    return await db_update_book(db, book_id, book)

@router.get("/{book_id}/summary", response_model=BookSummary)
async def get_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    return await db_get_summary(db, book_id)

@router.patch("/{book_id}/summary", response_model=BookSummary)
async def update_summary(book_id: int, summary: BookSummary, db: AsyncSession = Depends(get_db)):
    return await db_update_summary(db, book_id, summary) 