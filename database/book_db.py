from .db_connection import db
from logs.logger_config import logger
from pydantic import BaseModel, Field
from enum import Enum

class Genre(Enum):
    fiction = "Fiction"
    non_fiction  = "Non-Fiction"
    science = "Science"
    history = "History"
    other = "Other"

class Books(BaseModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    genre: Genre

class UpdateBooks(BaseModel):
    title: str | None = Field(default=None, max_length=50)
    author: str | None = Field(default=None, max_length=50)
    genre: Genre | None
    is_available: bool | None
    borrowed_by_member_id: int | None


class BookDB:
    def __init__(self):
        self.conn = db.conn
        
    def create_book(self, data: Books) -> int | None:
        data = data.model_dump()
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO books (title, author, genre) VALUES(%s, %s, %s)",
                (data["title"], data["author"], data["genre"].value)
            )
            self.conn.commit()
            logger.info("Created a new book on database")
            return cursor.lastrowid

    def get_all_books(self) -> list[dict] | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

    def get_book_by_id(self, book_id: int) -> dict | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            return cursor.fetchone()
    
    def update_book(self, book_id: int, data: dict) -> bool:
        if "genre" in data:
            data["genre"] = data["genre"].value
        
        parts = [f"{key} = %s" for key in data.keys()]
        join_parts = ", ".join(parts)
        
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                f"UPDATE books SET {join_parts} WHERE id = %s",
                list(data.values()) + [book_id]
            )
            self.conn.commit()
            logger.info("Updated book ID '%s' on database", book_id)
            return cursor.rowcount > 0
        
    def set_available(self, book_id: int, val: bool, member_id: int) -> bool:
        with self.conn.cursor(dictionary=True) as cursor:
            if val:
                cursor.execute(
                    """
                        UPDATE books SET is_available = TRUE,
                        borrowed_by_member_id = NULL WHERE id = %s
                    """,
                    (book_id,)
                )
                self.conn.commit()

            else:
                cursor.execute(
                    """
                        UPDATE books SET is_available = FALSE,
                        borrowed_by_member_id = %s WHERE id = %s
                    """,
                    (member_id, book_id)
                )
                self.conn.commit()
            logger.info("Set available book ID '%s' on database", book_id)
            return cursor.rowcount > 0
    
    def count_total_books(self) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")
            return cursor.fetchone()["COUNT(*)"]
        
    def count_available_books(self) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
            return cursor.fetchone()["COUNT(*)"]
    
    def count_borrowed_book(self) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
            return cursor.fetchone()["COUNT(*)"]

    def count_by_genre(self, genre: Genre | None = None) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre")
            return cursor.fetchall()
    
    def count_active_borrows_by_member(self, member_id: int) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(title) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
            return cursor.fetchone()["COUNT(title)"]
    
books_db = BookDB()