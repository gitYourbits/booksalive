"""Initial schema migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create books table
    op.create_table('books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('book_type', sa.String(length=50), nullable=False),
        sa.Column('isbn', sa.String(length=20), nullable=True),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('publisher', sa.String(length=255), nullable=True),
        sa.Column('total_pages', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True),
        sa.Column('cover_image_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=False)
    op.create_index(op.f('ix_books_isbn'), 'books', ['isbn'], unique=True)

    # Create chapters table
    op.create_table('chapters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('page_start', sa.Integer(), nullable=True),
        sa.Column('page_end', sa.Integer(), nullable=True),
        sa.Column('duration_minutes', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('book_id', 'chapter_number', name='uq_book_chapter_number')
    )
    op.create_index(op.f('ix_chapters_id'), 'chapters', ['id'], unique=False)
    op.create_index(op.f('ix_chapters_book_id'), 'chapters', ['book_id'], unique=False)

    # Create summaries table
    op.create_table('summaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.Column('key_points', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('real_life_examples', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('emotional_insights', sa.Text(), nullable=True),
        sa.Column('learning_objectives', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('difficulty_level', sa.Integer(), nullable=True),
        sa.Column('ai_generated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chapter_id', name='uq_summary_chapter')
    )
    op.create_index(op.f('ix_summaries_id'), 'summaries', ['id'], unique=False)
    op.create_index(op.f('ix_summaries_book_id'), 'summaries', ['book_id'], unique=False)
    op.create_index(op.f('ix_summaries_chapter_id'), 'summaries', ['chapter_id'], unique=False)

    # Create audios table
    op.create_table('audios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size_bytes', sa.Integer(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('audio_format', sa.String(length=10), nullable=True),
        sa.Column('quality', sa.String(length=20), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=True),
        sa.Column('processing_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chapter_id', name='uq_audio_chapter')
    )
    op.create_index(op.f('ix_audios_id'), 'audios', ['id'], unique=False)
    op.create_index(op.f('ix_audios_book_id'), 'audios', ['book_id'], unique=False)
    op.create_index(op.f('ix_audios_chapter_id'), 'audios', ['chapter_id'], unique=False)

    # Create doubts table
    op.create_table('doubts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('audio_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=True),
        sa.Column('audio_timestamp_start', sa.Float(), nullable=True),
        sa.Column('audio_timestamp_end', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('context_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['audio_id'], ['audios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doubts_id'), 'doubts', ['id'], unique=False)
    op.create_index(op.f('ix_doubts_book_id'), 'doubts', ['book_id'], unique=False)
    op.create_index(op.f('ix_doubts_chapter_id'), 'doubts', ['chapter_id'], unique=False)
    op.create_index(op.f('ix_doubts_audio_id'), 'doubts', ['audio_id'], unique=False)
    op.create_index(op.f('ix_doubts_user_id'), 'doubts', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_doubts_user_id'), table_name='doubts')
    op.drop_index(op.f('ix_doubts_audio_id'), table_name='doubts')
    op.drop_index(op.f('ix_doubts_chapter_id'), table_name='doubts')
    op.drop_index(op.f('ix_doubts_book_id'), table_name='doubts')
    op.drop_index(op.f('ix_doubts_id'), table_name='doubts')
    op.drop_table('doubts')

    op.drop_index(op.f('ix_audios_chapter_id'), table_name='audios')
    op.drop_index(op.f('ix_audios_book_id'), table_name='audios')
    op.drop_index(op.f('ix_audios_id'), table_name='audios')
    op.drop_table('audios')

    op.drop_index(op.f('ix_summaries_chapter_id'), table_name='summaries')
    op.drop_index(op.f('ix_summaries_book_id'), table_name='summaries')
    op.drop_index(op.f('ix_summaries_id'), table_name='summaries')
    op.drop_table('summaries')

    op.drop_index(op.f('ix_chapters_book_id'), table_name='chapters')
    op.drop_index(op.f('ix_chapters_id'), table_name='chapters')
    op.drop_table('chapters')

    op.drop_index(op.f('ix_books_isbn'), table_name='books')
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_table('books') 