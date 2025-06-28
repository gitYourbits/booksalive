from sqlalchemy import Column, Integer, String, Text, select, update, delete, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from typing import List, Optional, Sequence
from app.models.book import (
    BookCreate, BookUpdate, BookSummary as BookSummaryModel,
    ChapterCreate, ChapterUpdate, SummaryCreate, SummaryUpdate,
    AudioCreate, AudioUpdate, DoubtCreate, DoubtUpdate
)
from app.models.schema import Book, Chapter, Summary, Audio, Doubt, Base

# Async CRUD operations for Books
async def get_books(db: AsyncSession) -> Sequence[Book]:
    """Get all books from the database"""
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int) -> Optional[Book]:
    """Get a specific book by ID"""
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()

async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
    """Create a new book"""
    db_book = Book(
        title=book_data.title,
        author=book_data.author,
        description=book_data.description,
        book_type=book_data.book_type,
        isbn=book_data.isbn,
        publication_year=book_data.publication_year,
        publisher=book_data.publisher,
        total_pages=book_data.total_pages,
        language=book_data.language,
        cover_image_url=book_data.cover_image_url,
        is_active=book_data.is_active
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book_data: BookUpdate) -> Optional[Book]:
    """Update an existing book"""
    book = await get_book(db, book_id)
    if not book:
        return None
    
    update_data = book_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Book)
            .where(Book.id == book_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(book)
    
    return book

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    """Delete a book by ID"""
    book = await get_book(db, book_id)
    if not book:
        return False
    
    await db.delete(book)
    await db.commit()
    return True

# Async CRUD operations for Chapters
async def get_chapters(db: AsyncSession, book_id: int) -> Sequence[Chapter]:
    """Get all chapters for a book"""
    result = await db.execute(
        select(Chapter).where(Chapter.book_id == book_id).order_by(Chapter.chapter_number)
    )
    return result.scalars().all()

async def get_chapter(db: AsyncSession, chapter_id: int) -> Optional[Chapter]:
    """Get a specific chapter by ID"""
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    return result.scalar_one_or_none()

async def create_chapter(db: AsyncSession, book_id: int, chapter_data: ChapterCreate) -> Chapter:
    """Create a new chapter for a book"""
    db_chapter = Chapter(
        book_id=book_id,
        chapter_number=chapter_data.chapter_number,
        title=chapter_data.title,
        content=chapter_data.content,
        page_start=chapter_data.page_start,
        page_end=chapter_data.page_end,
        duration_minutes=chapter_data.duration_minutes
    )
    db.add(db_chapter)
    await db.commit()
    await db.refresh(db_chapter)
    return db_chapter

async def update_chapter(db: AsyncSession, chapter_id: int, chapter_data: ChapterUpdate) -> Optional[Chapter]:
    """Update an existing chapter"""
    chapter = await get_chapter(db, chapter_id)
    if not chapter:
        return None
    
    update_data = chapter_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Chapter)
            .where(Chapter.id == chapter_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(chapter)
    
    return chapter

async def delete_chapter(db: AsyncSession, chapter_id: int) -> bool:
    """Delete a chapter by ID"""
    chapter = await get_chapter(db, chapter_id)
    if not chapter:
        return False
    
    await db.delete(chapter)
    await db.commit()
    return True

# Async CRUD operations for Summaries
async def get_summary(db: AsyncSession, chapter_id: int) -> Optional[Summary]:
    """Get summary for a specific chapter"""
    result = await db.execute(
        select(Summary).where(Summary.chapter_id == chapter_id)
    )
    return result.scalar_one_or_none()

async def create_summary(db: AsyncSession, book_id: int, chapter_id: int, summary_data: SummaryCreate) -> Summary:
    """Create a new summary for a chapter"""
    db_summary = Summary(
        book_id=book_id,
        chapter_id=chapter_id,
        summary_text=summary_data.summary_text,
        key_points=summary_data.key_points,
        real_life_examples=summary_data.real_life_examples,
        emotional_insights=summary_data.emotional_insights,
        learning_objectives=summary_data.learning_objectives,
        difficulty_level=summary_data.difficulty_level
    )
    db.add(db_summary)
    await db.commit()
    await db.refresh(db_summary)
    return db_summary

async def update_summary(db: AsyncSession, chapter_id: int, summary_data: SummaryUpdate) -> Optional[Summary]:
    """Update an existing summary"""
    summary = await get_summary(db, chapter_id)
    if not summary:
        return None
    
    update_data = summary_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Summary)
            .where(Summary.chapter_id == chapter_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(summary)
    
    return summary

# Async CRUD operations for Audios
async def get_audio(db: AsyncSession, chapter_id: int) -> Optional[Audio]:
    """Get audio for a specific chapter"""
    result = await db.execute(
        select(Audio).where(Audio.chapter_id == chapter_id)
    )
    return result.scalar_one_or_none()

async def create_audio(db: AsyncSession, book_id: int, chapter_id: int, audio_data: AudioCreate) -> Audio:
    """Create a new audio for a chapter"""
    db_audio = Audio(
        book_id=book_id,
        chapter_id=chapter_id,
        file_path=audio_data.file_path,
        file_size_bytes=audio_data.file_size_bytes,
        duration_seconds=audio_data.duration_seconds,
        audio_format=audio_data.audio_format,
        quality=audio_data.quality,
        is_processed=audio_data.is_processed,
        processing_metadata=audio_data.processing_metadata
    )
    db.add(db_audio)
    await db.commit()
    await db.refresh(db_audio)
    return db_audio

async def update_audio(db: AsyncSession, chapter_id: int, audio_data: AudioUpdate) -> Optional[Audio]:
    """Update an existing audio"""
    audio = await get_audio(db, chapter_id)
    if not audio:
        return None
    
    update_data = audio_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Audio)
            .where(Audio.chapter_id == chapter_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(audio)
    
    return audio

# Async CRUD operations for Doubts
async def get_doubts(db: AsyncSession, chapter_id: int) -> Sequence[Doubt]:
    """Get all doubts for a chapter"""
    result = await db.execute(
        select(Doubt).where(Doubt.chapter_id == chapter_id).order_by(Doubt.created_at.desc())
    )
    return result.scalars().all()

async def get_doubt(db: AsyncSession, doubt_id: int) -> Optional[Doubt]:
    """Get a specific doubt by ID"""
    result = await db.execute(select(Doubt).where(Doubt.id == doubt_id))
    return result.scalar_one_or_none()

async def create_doubt(db: AsyncSession, book_id: int, chapter_id: int, audio_id: int, doubt_data: DoubtCreate) -> Doubt:
    """Create a new doubt"""
    db_doubt = Doubt(
        book_id=book_id,
        chapter_id=chapter_id,
        audio_id=audio_id,
        user_id=doubt_data.user_id,
        question=doubt_data.question,
        ai_response=doubt_data.ai_response,
        audio_timestamp_start=doubt_data.audio_timestamp_start,
        audio_timestamp_end=doubt_data.audio_timestamp_end,
        status=doubt_data.status,
        confidence_score=doubt_data.confidence_score,
        context_data=doubt_data.context_data
    )
    db.add(db_doubt)
    await db.commit()
    await db.refresh(db_doubt)
    return db_doubt

async def update_doubt(db: AsyncSession, doubt_id: int, doubt_data: DoubtUpdate) -> Optional[Doubt]:
    """Update an existing doubt"""
    doubt = await get_doubt(db, doubt_id)
    if not doubt:
        return None
    
    update_data = doubt_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Doubt)
            .where(Doubt.id == doubt_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(doubt)
    
    return doubt

async def delete_doubt(db: AsyncSession, doubt_id: int) -> bool:
    """Delete a doubt by ID"""
    doubt = await get_doubt(db, doubt_id)
    if not doubt:
        return False
    
    await db.delete(doubt)
    await db.commit()
    return True

# Legacy function for backward compatibility
async def update_summary_legacy(db: AsyncSession, book_id: int, summary_data: BookSummaryModel) -> Optional[Summary]:
    """Legacy function for updating summary (for backward compatibility)"""
    # This would need to be updated based on your specific use case
    # For now, returning None as the new schema requires chapter_id
    return None 