from .db_connection import db
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
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def create_book(self, data: Books) -> int | None:
        logger.info("Start... create a new book on database")
        
        data = data.model_dump()
        self.cursor.execute(
            "INSERT INTO books (title, author, genre) VALUES(%s, %s, %s)",
            (data.title, data.author, data.genre)
        )
        self.conn.commit()
        new_id = self.cursor.lastrowid
        self.close()

        return new_id
    
    def get_all_books(self) -> list[dict] | None:
        logger("Start... get all books on database")

        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        self.close()

        return rows
    
    def get_book_by_id(self, book_id: int) -> dict | None:
        logger.info("Start... get book by id database")

        self.cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        row = self.cursor.fetchone()
        self.close()

        return row
    
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
        updated = self.cursor.rowcount > 0
        self.close()

        return updated
    
    def set_available(self, book_id: int, val: bool, member_id: int) -> bool:
        logger.info("Start... update available book on database")
        
        if val:
            self.cursor.execute(
                """
                    UPDATE books SET is_available = TRUE,
                    borrowed_by_member_id IS NULL WHERE id = %s
                """,
                (book_id,)
            )
            self.conn.commit()

        else:
            self.cursor.execute(
                """
                    UPDATE books SET is_available = FALSE,
                    borrowed_by_member_id = %s WHERE id = %s
                """,
                (member_id, book_id)
            )
            self.conn.commit()
        availabled = self.cursor.rowcount > 0
        self.close()
        
        return availabled
    
    def count_total_books(self) -> int | None:
        logger.info("Start... Get all total books in the database")
        
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()
        self.close()

        return total_books
    
    def count_available_books(self) -> int | None:
        logger.info("Start... Get all books that available from database")

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = TRUE")
        available = self.cursor.fetchone()
        self.close()

        return available
    
    def count_borrowed_book(self) -> int | None:
        logger.info("Start... get total of books that borrowed from database")

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = FALSE")
        borrowed = self.cursor.fetchone()
        self.close()

        return borrowed
    
    def count_by_genre(self, genre: Genre) -> int | None:
        logger.info("Start... Get total books by genre '%s' from database", genre)

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s", genre)
        total_genre = self.cursor.fetchone()
        self.close()

        return total_genre
    
    def count_active_borrows_by_member(self, member_id: int) -> int | None:
        logger.info("Start... Get total books of a member ID from database %s", member_id)
        
        self.cursor.execute("SELECT COUNT(title) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
        total_member_book = self.cursor.fetchone()
        self.close()

        return total_member_book
    
    def close(self):
        self.conn.close()
        self.cursor.close()