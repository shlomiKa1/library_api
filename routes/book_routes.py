from logs.logger_config import logger
from database.book_db import BookDB, Books
from fastapi import APIRouter, HTTPException


router_books = APIRouter()
books = BookDB()

@router_books.post("", status_code=201)
def add_book(new_book: Books):
    logger.info("Start... create book from server")

    new_id = books.create_book(new_book)
    if not new_id:
        logger.warning("Was an error to create a new book")
        raise HTTPException(500, "Failed to create book")
    logger.info("Book createld successfully, the new ID '%s'", new_id)
    
    return {"Message": "Book created successfully"}

@router_books.get("", status_code=200)
def get_books():
    logger.info("Start... get all books from server")
    all_books = books.get_all_books()
    logger.info("Return '%s' books from database", len(all_books))
    
    return {"Message": all_books}

@router_books.get("/{id}")
def book_by_id(id: int):
    logger.info("Start... get book by ID '%s' from server", id)

    book = books.get_book_by_id(id)
    if not book:
        raise HTTPException(404, "ID not found")
    logger.info("Return book by ID '%s'", id)
    return {"Message": book}
 