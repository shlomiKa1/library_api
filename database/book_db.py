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
        self.conn = db.get_connection()

    def create_book(self, data: Books) -> int | None:
        logger.info("Start... create a new book on database")
        
        data = data.model_dump()
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO books (title, author, genre) VALUES(%s, %s, %s)",
                (data["title"], data["author"], data["genre"].value)
            )
            self.conn.commit()
            new_id = cursor.lastrowid

        return new_id
    
    def get_all_books(self) -> list[dict] | None:
        logger.info("Start... get all books on database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()

        return rows
    
    def get_book_by_id(self, book_id: int) -> dict | None:
        logger.info("Start... get book by id database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            row = cursor.fetchone()

        return row
    
    def update_book(self, book_id: int, data: dict) -> bool:
        logger.info("Start... update book on database")

        # data = data.model_dump(exclude_unset=True)
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
            updated = cursor.rowcount > 0
        
        return updated
    
    def set_available(self, book_id: int, val: bool, member_id: int) -> bool:
        logger.info("Start... update available book on database")
        
        with self.conn.cursor(dictionary=True) as cursor:
            if val:
                cursor.execute(
                    """
                        UPDATE books SET is_available = TRUE,
                        borrowed_by_member_id IS NULL WHERE id = %s
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
            availabled = cursor.rowcount > 0
        
        return availabled
    
    def count_total_books(self) -> int | None:
        logger.info("Start... Get all total books in the database")
        
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = self.cursor.fetchone()
        
        return total_books
    
    def count_available_books(self) -> int | None:
        logger.info("Start... Get all books that available from database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
            available = cursor.fetchone()
        
        return available
    
    def count_borrowed_book(self) -> int | None:
        logger.info("Start... get total of books that borrowed from database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
            borrowed = cursor.fetchone()

        return borrowed
    
    def count_by_genre(self, genre: Genre) -> int | None:
        logger.info("Start... Get total books by genre '%s' from database", genre)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s", genre)
            total_genre = cursor.fetchone()

        return total_genre
    
    def count_active_borrows_by_member(self, member_id: int) -> int | None:
        logger.info("Start... Get total books of a member ID from database %s", member_id)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(title) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
            total_member_book = cursor.fetchone()
        
        return total_member_book
    
books_db = BookDB()