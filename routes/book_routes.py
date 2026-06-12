from logs.logger_config import logger
from database.book_db import BookDB, Books
from fastapi import APIRouter, exception_handlers, middleware


router_books = APIRouter()
books = BookDB()

@router_books.post("")
def add_book(new_book: Books):
    logger.info("Start... create book from server")

    new_id = books.create_book(new_book)
    if not new_id:
        logger.warning("Was an error to create a new book")
    logger.info("Book createld successfully, the new ID '%s'", new_id)
    
    return {"Message": "Book created successfully"}

