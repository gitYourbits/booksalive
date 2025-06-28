#!/usr/bin/env python3
"""
Test script to verify the Booksalive setup
Useful for validating the system is working correctly after changes or deployments.
"""

import asyncio
import sys
from sqlalchemy import text
from app.db import get_db
from app.models.schema import Base
from app.core.config import DATABASE_URL

async def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        async for db in get_db():
            # Test basic connection
            result = await db.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            
            # Test schema import
            print("Testing schema import...")
            from app.models.schema import Book, Chapter, Summary, Audio, Doubt
            print("✅ All models imported successfully")
            
            # Test table creation (if database is empty)
            try:
                result = await db.execute(text("SELECT COUNT(*) FROM books"))
                count = result.scalar()
                print(f"✅ Books table exists with {count} records")
            except Exception as e:
                print(f"⚠️  Books table not found (run migrations first): {e}")
            
            break
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

async def test_api_imports():
    """Test API imports"""
    print("Testing API imports...")
    try:
        from app.api.books import router
        from app.api.health import router as health_router
        print("✅ API routes imported successfully")
        return True
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False

async def test_models():
    """Test model imports and validation"""
    print("Testing models...")
    try:
        from app.models.book import BookCreate, ChapterCreate, SummaryCreate
        from app.models.schema import BookType, AudioFormat, DoubtStatus
        
        # Test enum values
        print(f"✅ Book types: {[bt.value for bt in BookType]}")
        print(f"✅ Audio formats: {[af.value for af in AudioFormat]}")
        print(f"✅ Doubt statuses: {[ds.value for ds in DoubtStatus]}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

async def test_fastapi_app():
    """Test FastAPI application"""
    print("Testing FastAPI application...")
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
        
        # Test that routes are registered (just count them)
        route_count = len(app.routes)
        print(f"✅ Found {route_count} registered routes")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        return False

async def test_schema_relationships():
    """Test schema relationships"""
    print("Testing schema relationships...")
    try:
        from app.models.schema import Book, Chapter, Summary, Audio, Doubt
        
        # Test that relationships are properly defined
        assert hasattr(Book, 'chapters'), "Book should have chapters relationship"
        assert hasattr(Book, 'summaries'), "Book should have summaries relationship"
        assert hasattr(Book, 'audios'), "Book should have audios relationship"
        assert hasattr(Book, 'doubts'), "Book should have doubts relationship"
        
        assert hasattr(Chapter, 'book'), "Chapter should have book relationship"
        assert hasattr(Chapter, 'summary'), "Chapter should have summary relationship"
        assert hasattr(Chapter, 'audio'), "Chapter should have audio relationship"
        assert hasattr(Chapter, 'doubts'), "Chapter should have doubts relationship"
        
        print("✅ All schema relationships properly defined")
        return True
    except Exception as e:
        print(f"❌ Schema relationships test failed: {e}")
        return False

async def test_pydantic_models():
    """Test Pydantic model validation"""
    print("Testing Pydantic models...")
    try:
        from app.models.book import BookCreate, ChapterCreate, SummaryCreate, AudioCreate, DoubtCreate
        from app.models.schema import BookType
        
        # Test BookCreate validation
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "description": "Test description",
            "book_type": BookType.SELF_HELP
        }
        book = BookCreate(**book_data)
        print("✅ BookCreate validation successful")
        
        # Test ChapterCreate validation
        chapter_data = {
            "chapter_number": 1,
            "title": "Test Chapter",
            "content": "Test content"
        }
        chapter = ChapterCreate(**chapter_data)
        print("✅ ChapterCreate validation successful")
        
        # Test SummaryCreate validation
        summary_data = {
            "summary_text": "Test summary",
            "key_points": ["Point 1", "Point 2"],
            "difficulty_level": 2
        }
        summary = SummaryCreate(**summary_data)
        print("✅ SummaryCreate validation successful")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic model test failed: {e}")
        return False

async def test_configuration():
    """Test configuration settings"""
    print("Testing configuration...")
    try:
        from app.core.config import DATABASE_URL, POSTGRES_USER, POSTGRES_DB
        
        # Check if configuration is loaded
        assert DATABASE_URL, "DATABASE_URL should be configured"
        assert POSTGRES_USER, "POSTGRES_USER should be configured"
        assert POSTGRES_DB, "POSTGRES_DB should be configured"
        
        print("✅ Configuration loaded successfully")
        print(f"   Database: {POSTGRES_DB}")
        print(f"   User: {POSTGRES_USER}")
        print(f"   URL: {DATABASE_URL[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 Testing Booksalive Setup")
    print("=" * 50)
    
    # Test database connection
    db_ok = await test_database_connection()
    
    # Test API imports
    api_ok = await test_api_imports()
    
    # Test models
    models_ok = await test_models()
    
    # Test FastAPI app
    app_ok = await test_fastapi_app()
    
    # Test schema relationships
    schema_ok = await test_schema_relationships()
    
    # Test Pydantic models
    pydantic_ok = await test_pydantic_models()
    
    # Test configuration
    config_ok = await test_configuration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Database: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"API: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"FastAPI App: {'✅ PASS' if app_ok else '❌ FAIL'}")
    print(f"Schema Relationships: {'✅ PASS' if schema_ok else '❌ FAIL'}")
    print(f"Pydantic Models: {'✅ PASS' if pydantic_ok else '❌ FAIL'}")
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    
    passed_tests = sum([db_ok, api_ok, models_ok, app_ok, schema_ok, pydantic_ok, config_ok])
    total_tests = 7
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Booksalive is ready to use.")
        print("\nNext steps:")
        print("1. Start PostgreSQL if not running")
        print("2. Run: alembic upgrade head")
        print("3. Run: uvicorn app.main:app --reload")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        if not db_ok:
            print("Note: Database test failure is expected if PostgreSQL is not running")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 