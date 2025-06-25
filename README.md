# Booksalive

## Project Vision
Booksalive is an interactive, emotionally intelligent audiobook platform that transforms passive listening into active learning. It features emotionally expressive AI narration, real-time explanations, mid-dictation doubt solving using fine-tuned LLMs, and personalized learning through real-life scenario simulations. The long-term vision is to build a creator ecosystem where authors can publish, explain their books to AI, track user engagement, and foster direct reader communities.

## Features
- Emotionally expressive AI audiobook narration
- Real-time explanations and doubt solving
- Personalized learning and scenario simulations
- Caching and on-device asset storage for scalability
- Creator tools for authors and publishers

## Tech Stack
- FastAPI (Python backend)
- PostgreSQL (database)
- SQLAlchemy (async ORM)
- Pydantic (data validation)

## Getting Started
1. Clone the repository
2. Create a `.env` file in the root with your PostgreSQL credentials (see below)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI app:
   ```bash
   uvicorn app.main:app --reload
   ```

## .env Example
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=booksalive
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## License
MIT (or specify your license)