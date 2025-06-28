"""
Database Schema Design for Booksalive

This module defines the SQLAlchemy models for the Booksalive application.
The schema supports:
- Books with metadata and chapters
- Chapter summaries with AI-generated content
- Audio files linked to summaries
- User doubts and AI responses with timestamp tracking
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List
from enum import Enum

Base = declarative_base()

class BookType(str, Enum):
    SELF_HELP = "self_help"
    ENTERTAINMENT = "entertainment"
    LITERATURE = "literature"
    NOVEL = "novel"
    EDUCATIONAL = "educational"
    BUSINESS = "business"
    FICTION = "fiction"
    NON_FICTION = "non_fiction"

class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"
    OGG = "ogg"

class DoubtStatus(str, Enum):
    PENDING = "pending"
    ANSWERED = "answered"
    RESOLVED = "resolved"

# Parent Table: Books
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    book_type = Column(String(50), nullable=False, default=BookType.NON_FICTION)
    isbn = Column(String(20), unique=True, index=True)
    publication_year = Column(Integer)
    publisher = Column(String(255))
    total_pages = Column(Integer)
    language = Column(String(10), default="en")
    cover_image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="book", cascade="all, delete-orphan")
    audios = relationship("Audio", back_populates="book", cascade="all, delete-orphan")
    doubts = relationship("Doubt", back_populates="book", cascade="all, delete-orphan")

# Child Table: Chapters
class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    page_start = Column(Integer)
    page_end = Column(Integer)
    duration_minutes = Column(Float)  # Estimated reading time
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="chapters")
    summary = relationship("Summary", back_populates="chapter", uselist=False, cascade="all, delete-orphan")
    audio = relationship("Audio", back_populates="chapter", uselist=False, cascade="all, delete-orphan")
    doubts = relationship("Doubt", back_populates="chapter", cascade="all, delete-orphan")
    
    # Composite unique constraint
    __table_args__ = (
        # Ensure unique chapter numbers per book
        # This will be handled in the migration
    )

# Child Table: Summaries (one per chapter)
class Summary(Base):
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, unique=True)
    summary_text = Column(Text, nullable=False)
    key_points = Column(JSON)  # Store as JSON array of key points
    real_life_examples = Column(JSON)  # Store as JSON array of examples
    emotional_insights = Column(Text)  # AI-generated emotional analysis
    learning_objectives = Column(JSON)  # Store as JSON array of objectives
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    ai_generated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="summaries")
    chapter = relationship("Chapter", back_populates="summary")

# Child Table: Audios (stores narration files)
class Audio(Base):
    __tablename__ = "audios"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, unique=True)
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer)
    duration_seconds = Column(Float)
    audio_format = Column(String(10), default=AudioFormat.MP3)
    quality = Column(String(20), default="high")  # low, medium, high
    is_processed = Column(Boolean, default=False)
    processing_metadata = Column(JSON)  # Store processing info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="audios")
    chapter = relationship("Chapter", back_populates="audio")
    doubts = relationship("Doubt", back_populates="audio", cascade="all, delete-orphan")

# Child Table: Doubts (user questions and AI responses)
class Doubt(Base):
    __tablename__ = "doubts"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    audio_id = Column(Integer, ForeignKey("audios.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(100), nullable=False, index=True)  # Could be UUID or user identifier
    question = Column(Text, nullable=False)
    ai_response = Column(Text)
    audio_timestamp_start = Column(Float)  # Start time in seconds
    audio_timestamp_end = Column(Float)    # End time in seconds
    status = Column(String(20), default=DoubtStatus.PENDING)
    confidence_score = Column(Float)  # AI confidence in the response
    context_data = Column(JSON)  # Additional context for the doubt
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    book = relationship("Book", back_populates="doubts")
    chapter = relationship("Chapter", back_populates="doubts")
    audio = relationship("Audio", back_populates="doubts") 