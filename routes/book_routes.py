from logs.logger_config import logger
from database.book_db import books_db, Books, UpdateBooks
from database.member_db import member_db
from fastapi import APIRouter, HTTPException
from config import COUNT_BOOKS
from routes.member_routes import member_by_id


router_books = APIRouter()

@router_books.post("", status_code=201)
def add_book(new_book: Books):
    logger.info("Start... create book from server")

    new_id = books_db.create_book(new_book)
    if not new_id:
        logger.warning("Was an error to create a new book")
        raise HTTPException(500, "Failed to create book")
    logger.info("Book created successfully, the new ID '%s'", new_id)
    
    return {"Message": "Book created successfully"}

@router_books.get("", status_code=200)
def get_books():
    logger.info("Start... get all books from server")
    all_books = books_db.get_all_books()
    logger.info("Return '%s' books from database", len(all_books))
    
    return {"Message": all_books}

@router_books.get("/{id}")
def book_by_id(id: int):
    logger.info("Start... get book by ID '%s' from server", id)

    book = books_db.get_book_by_id(id)
    if not book:
        raise HTTPException(404, "Book not found")
    logger.info("Return book by ID '%s'", id)
    return {"Message": book}

@router_books.patch("/{id}")
def update_book(id: int, data: UpdateBooks):
    logger.info("Start... update book by ID '%s' from server", id)
    
    if not data:
        raise HTTPException(400, "Error with the detail")
    
    updated = books_db.update_book(id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(404, "Book not found")
    logger.info("Book ID '%s' updated successfully", id)
    return {"Message": f"Book ID updated {id} successfully"}

@router_books.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.info("Start... borrow book - server")

    member =member_by_id(member_id)
    book = book_by_id(id)

    if not member["Message"]["is_active"]:
        raise HTTPException(400, "Member is not active")
    
    if not book["Message"]["is_available"]:
        raise HTTPException(400, "Book is not available")

    count_book = books_db.count_active_borrows_by_member(member_id)

    if count_book >= COUNT_BOOKS:
        raise HTTPException(400, " Member has reached maximum borrows")
    
    if books_db.set_available(id, False, member_id):
        if member_db.increment_borrows(member_id):
            logger.info("Book '%s' is not available", id)
            return {"Message": f"Book ID '{id}' is borrowed by member ID '{member_id}'"}
    raise
    
@router_books.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.info("Start... return book ID '%s' & member ID '%s' - server", id, member_id)

    member_by_id(member_id)
    book = book_by_id(id)
    
    if book["Message"]["is_available"]:
        raise HTTPException(400, "Book is available")
    
    if not book["Message"]["borrowed_by_member_id"] == member_id:
        raise HTTPException(404, "Book is not borrowed by this member")
    
    if books_db.set_available(id, True, member_id):
        logger.info("Book ID '%s' return by member ID '%s'", id, member_id)
        return {"Message": f"Member ID '{member_id}' return the book ID '{id}'"}