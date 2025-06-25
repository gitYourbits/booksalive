from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, books

app = FastAPI(title="Booksalive API", version="1.0.0")

# CORS setup (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(books.router) 