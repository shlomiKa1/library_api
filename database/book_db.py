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
        self.cursor = self.conn.cursor(dictionary=True)

    def create_book(self, data: Books) -> int | None:
        logger.info("Start... create a new book on database")
        
        data = data.model_dump()
        self.cursor.execute(
            "INSERT INTO books (title, author, genre) VALUES(%s, %s, %s)",
            (data.title, data.author, data.genre)
        )
        self.conn.commit()

        return self.cursor.lastrowid
    
    def get_all_books(self) -> list[dict] | None:
        logger("Start... get all books on database")

        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()
    
    def get_book_by_id(self, book_id: int) -> dict | None:
        logger.info("Start... get book by id database")

        self.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        return self.cursor.fetchone()
    
    def update_book(self, book_id: int, data: UpdateBooks) -> bool:
        logger.info("Start... update book on database")

        data = data.model_dump(exclude_unset=True)
        parts = [f"{key} = %s" for key in data.keys()]
        join_parts = ", ".join(parts)

        self.cursor.execute(
            "UPDATE books SET %s WHERE id = %s",
            (join_parts, list(data.values()) + [book_id])
        )
        self.conn.commit()

        return self.cursor.rowcount > 0
        