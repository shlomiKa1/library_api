from .db_connection import get_connection
from logs.logger_config import logger
from pydantic import BaseModel, Field
from enum import Enum

class Genre(Enum):
    fiction = "Fiction"
    non_fiction  = "Non-fiction"
    science = "science"
    history = "History"
    other = "other"

class Books(BaseModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    genre: Genre

class UpdateBooks(BaseModel):
    title: str | None = Field(max_length=50)
    author: str | None = Field(max_length=50)
    genre: Genre | None


class BookDB:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def create_book(self, data: Books):
        logger.info("Start create a new book...")

        self.cursor.execute(
            "INSERT INTO books (title, author, genre) VALUES(%s, %s, %s)",
            (data.title, data.author, data.genre)
        )
        self.conn.commit()

        return self.cursor.lastrowid

    
        