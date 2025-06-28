from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

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

# Base models
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    book_type: BookType = BookType.NON_FICTION
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1800, le=2100)
    publisher: Optional[str] = Field(None, max_length=255)
    total_pages: Optional[int] = Field(None, ge=1)
    language: str = Field(default="en", max_length=10)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True

class ChapterBase(BaseModel):
    chapter_number: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    page_start: Optional[int] = Field(None, ge=1)
    page_end: Optional[int] = Field(None, ge=1)
    duration_minutes: Optional[float] = Field(None, ge=0)

class SummaryBase(BaseModel):
    summary_text: str = Field(..., min_length=1)
    key_points: Optional[List[str]] = None
    real_life_examples: Optional[List[str]] = None
    emotional_insights: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    difficulty_level: int = Field(default=1, ge=1, le=5)

class AudioBase(BaseModel):
    file_path: str = Field(..., min_length=1, max_length=500)
    file_size_bytes: Optional[int] = Field(None, ge=0)
    duration_seconds: Optional[float] = Field(None, ge=0)
    audio_format: AudioFormat = AudioFormat.MP3
    quality: str = Field(default="high", max_length=20)
    is_processed: bool = False
    processing_metadata: Optional[Dict[str, Any]] = None

class DoubtBase(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    question: str = Field(..., min_length=1)
    ai_response: Optional[str] = None
    audio_timestamp_start: Optional[float] = Field(None, ge=0)
    audio_timestamp_end: Optional[float] = Field(None, ge=0)
    status: DoubtStatus = DoubtStatus.PENDING
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    context_data: Optional[Dict[str, Any]] = None

# Create models
class BookCreate(BookBase):
    pass

class ChapterCreate(ChapterBase):
    pass

class SummaryCreate(SummaryBase):
    pass

class AudioCreate(AudioBase):
    pass

class DoubtCreate(DoubtBase):
    pass

# Update models
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    book_type: Optional[BookType] = None
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1800, le=2100)
    publisher: Optional[str] = Field(None, max_length=255)
    total_pages: Optional[int] = Field(None, ge=1)
    language: Optional[str] = Field(None, max_length=10)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class ChapterUpdate(BaseModel):
    chapter_number: Optional[int] = Field(None, ge=1)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    page_start: Optional[int] = Field(None, ge=1)
    page_end: Optional[int] = Field(None, ge=1)
    duration_minutes: Optional[float] = Field(None, ge=0)

class SummaryUpdate(BaseModel):
    summary_text: Optional[str] = Field(None, min_length=1)
    key_points: Optional[List[str]] = None
    real_life_examples: Optional[List[str]] = None
    emotional_insights: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)

class AudioUpdate(BaseModel):
    file_path: Optional[str] = Field(None, min_length=1, max_length=500)
    file_size_bytes: Optional[int] = Field(None, ge=0)
    duration_seconds: Optional[float] = Field(None, ge=0)
    audio_format: Optional[AudioFormat] = None
    quality: Optional[str] = Field(None, max_length=20)
    is_processed: Optional[bool] = None
    processing_metadata: Optional[Dict[str, Any]] = None

class DoubtUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1)
    ai_response: Optional[str] = None
    audio_timestamp_start: Optional[float] = Field(None, ge=0)
    audio_timestamp_end: Optional[float] = Field(None, ge=0)
    status: Optional[DoubtStatus] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    context_data: Optional[Dict[str, Any]] = None

# Response models
class Chapter(ChapterBase):
    id: int
    book_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Summary(SummaryBase):
    id: int
    book_id: int
    chapter_id: int
    ai_generated_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Audio(AudioBase):
    id: int
    book_id: int
    chapter_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Doubt(DoubtBase):
    id: int
    book_id: int
    chapter_id: int
    audio_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    chapters: Optional[List[Chapter]] = []
    summaries: Optional[List[Summary]] = []
    audios: Optional[List[Audio]] = []
    doubts: Optional[List[Doubt]] = []

    class Config:
        from_attributes = True

# Legacy models for backward compatibility
class BookSummary(BaseModel):
    summary: str 