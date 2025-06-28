from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import (
    Book, BookCreate, BookUpdate, BookSummary,
    Chapter, ChapterCreate, ChapterUpdate,
    Summary, SummaryCreate, SummaryUpdate,
    Audio, AudioCreate, AudioUpdate,
    Doubt, DoubtCreate, DoubtUpdate
)
from app.db.books import (
    get_books as db_get_books, get_book as db_get_book, create_book as db_create_book, 
    update_book as db_update_book, delete_book as db_delete_book,
    get_chapters as db_get_chapters, get_chapter as db_get_chapter, create_chapter as db_create_chapter,
    update_chapter as db_update_chapter, delete_chapter as db_delete_chapter,
    get_summary as db_get_summary, create_summary as db_create_summary, update_summary as db_update_summary,
    get_audio as db_get_audio, create_audio as db_create_audio, update_audio as db_update_audio,
    get_doubts as db_get_doubts, get_doubt as db_get_doubt, create_doubt as db_create_doubt,
    update_doubt as db_update_doubt, delete_doubt as db_delete_doubt
)
from app.db import get_db

router = APIRouter(prefix="/books", tags=["Books"])

# Book routes
@router.get("/", response_model=List[Book])
async def get_books(db: AsyncSession = Depends(get_db)):
    """Get all books"""
    try:
        return await db_get_books(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch books: {str(e)}")

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific book by ID"""
    try:
        book = await db_get_book(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch book: {str(e)}")

@router.post("/", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """Create a new book"""
    try:
        return await db_create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")

@router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing book"""
    try:
        updated_book = await db_update_book(db, book_id, book)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update book: {str(e)}")

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a book"""
    try:
        success = await db_delete_book(db, book_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete book: {str(e)}")

# Chapter routes
@router.get("/{book_id}/chapters", response_model=List[Chapter])
async def get_chapters(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get all chapters for a book"""
    try:
        # Verify book exists
        book = await db_get_book(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return await db_get_chapters(db, book_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chapters: {str(e)}")

@router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific chapter by ID"""
    try:
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return chapter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chapter: {str(e)}")

@router.post("/{book_id}/chapters", response_model=Chapter)
async def create_chapter(book_id: int, chapter: ChapterCreate, db: AsyncSession = Depends(get_db)):
    """Create a new chapter for a book"""
    try:
        # Verify book exists
        book = await db_get_book(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return await db_create_chapter(db, book_id, chapter)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create chapter: {str(e)}")

@router.patch("/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(chapter_id: int, chapter: ChapterUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing chapter"""
    try:
        updated_chapter = await db_update_chapter(db, chapter_id, chapter)
        if not updated_chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return updated_chapter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update chapter: {str(e)}")

@router.delete("/chapters/{chapter_id}")
async def delete_chapter(chapter_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a chapter"""
    try:
        success = await db_delete_chapter(db, chapter_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return {"message": "Chapter deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete chapter: {str(e)}")

# Summary routes
@router.get("/chapters/{chapter_id}/summary", response_model=Summary)
async def get_summary(chapter_id: int, db: AsyncSession = Depends(get_db)):
    """Get summary for a specific chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        summary = await db_get_summary(db, chapter_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch summary: {str(e)}")

@router.post("/chapters/{chapter_id}/summary", response_model=Summary)
async def create_summary(chapter_id: int, summary: SummaryCreate, db: AsyncSession = Depends(get_db)):
    """Create a new summary for a chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        return await db_create_summary(db, chapter.book_id, chapter_id, summary)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create summary: {str(e)}")

@router.patch("/chapters/{chapter_id}/summary", response_model=Summary)
async def update_summary(chapter_id: int, summary: SummaryUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing summary"""
    try:
        updated_summary = await db_update_summary(db, chapter_id, summary)
        if not updated_summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        return updated_summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update summary: {str(e)}")

# Audio routes
@router.get("/chapters/{chapter_id}/audio", response_model=Audio)
async def get_audio(chapter_id: int, db: AsyncSession = Depends(get_db)):
    """Get audio for a specific chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        audio = await db_get_audio(db, chapter_id)
        if not audio:
            raise HTTPException(status_code=404, detail="Audio not found")
        return audio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch audio: {str(e)}")

@router.post("/chapters/{chapter_id}/audio", response_model=Audio)
async def create_audio(chapter_id: int, audio: AudioCreate, db: AsyncSession = Depends(get_db)):
    """Create a new audio for a chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        return await db_create_audio(db, chapter.book_id, chapter_id, audio)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create audio: {str(e)}")

@router.patch("/chapters/{chapter_id}/audio", response_model=Audio)
async def update_audio(chapter_id: int, audio: AudioUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing audio"""
    try:
        updated_audio = await db_update_audio(db, chapter_id, audio)
        if not updated_audio:
            raise HTTPException(status_code=404, detail="Audio not found")
        return updated_audio
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update audio: {str(e)}")

# Doubt routes
@router.get("/chapters/{chapter_id}/doubts", response_model=List[Doubt])
async def get_doubts(chapter_id: int, db: AsyncSession = Depends(get_db)):
    """Get all doubts for a chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        return await db_get_doubts(db, chapter_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doubts: {str(e)}")

@router.get("/doubts/{doubt_id}", response_model=Doubt)
async def get_doubt(doubt_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific doubt by ID"""
    try:
        doubt = await db_get_doubt(db, doubt_id)
        if not doubt:
            raise HTTPException(status_code=404, detail="Doubt not found")
        return doubt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doubt: {str(e)}")

@router.post("/chapters/{chapter_id}/doubts", response_model=Doubt)
async def create_doubt(chapter_id: int, doubt: DoubtCreate, db: AsyncSession = Depends(get_db)):
    """Create a new doubt for a chapter"""
    try:
        # Verify chapter exists
        chapter = await db_get_chapter(db, chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        
        # Verify audio exists
        audio = await db_get_audio(db, chapter_id)
        if not audio:
            raise HTTPException(status_code=404, detail="Audio not found for this chapter")
        
        return await db_create_doubt(db, chapter.book_id, chapter_id, audio.id, doubt)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create doubt: {str(e)}")

@router.patch("/doubts/{doubt_id}", response_model=Doubt)
async def update_doubt(doubt_id: int, doubt: DoubtUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing doubt"""
    try:
        updated_doubt = await db_update_doubt(db, doubt_id, doubt)
        if not updated_doubt:
            raise HTTPException(status_code=404, detail="Doubt not found")
        return updated_doubt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update doubt: {str(e)}")

@router.delete("/doubts/{doubt_id}")
async def delete_doubt(doubt_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a doubt"""
    try:
        success = await db_delete_doubt(db, doubt_id)
        if not success:
            raise HTTPException(status_code=404, detail="Doubt not found")
        return {"message": "Doubt deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete doubt: {str(e)}")

# Legacy routes for backward compatibility
@router.get("/{book_id}/summary", response_model=BookSummary)
async def get_summary_legacy(book_id: int, db: AsyncSession = Depends(get_db)):
    """Legacy endpoint: Get summary for a specific book (deprecated)"""
    try:
        # First check if book exists
        book = await db_get_book(db, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # For legacy compatibility, return a simple summary
        # In the new schema, summaries are per-chapter
        return BookSummary(summary="This endpoint is deprecated. Use /chapters/{chapter_id}/summary instead.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch summary: {str(e)}")

@router.patch("/{book_id}/summary", response_model=BookSummary)
async def update_summary_legacy(book_id: int, summary: BookSummary, db: AsyncSession = Depends(get_db)):
    """Legacy endpoint: Update summary for a book (deprecated)"""
    try:
        # For legacy compatibility, just return the summary
        # In the new schema, summaries are per-chapter
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update summary: {str(e)}") 