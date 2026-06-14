from logs.logger_config import logger
from database.book_db import books_db
from database.member_db import member_db
from fastapi import APIRouter, HTTPException


router_report = APIRouter()

@router_report.get("/summary")
def summary():
    logger.info("Start... summary reports")
    
    total_books =  books_db.count_total_books()
    available_books = books_db.count_available_books()
    currently_borrowed = books_db.count_borrowed_book()
    active_members = member_db.count_active_members()

    logger.info("Return total_books: %s, available_books: %s, currently_borrowed: %s, active_members", 
                (total_books, available_books, currently_borrowed, active_members))
    return {
        "total_books": total_books,
        "available_books": available_books,
        "currently_borrowed": currently_borrowed,
        "active_members": active_members
    }

@router_report.get("/books-by-genre")
def books_by_genre():
    logger.info("get total by genre")

    genres = {}
    
    for val in books_db.count_by_genre():
        genres[val["genre"]] = val["COUNT(*)"]
    logger.info("Return total genre %s", genres)
    return genres

@router_report.get("/top-member")
def get_top_member():
    logger.info("Start get top member")
    member = member_db.get_top_member()
    
    if not member:
        raise HTTPException(400, "There is not a member")
    
    logger.info("Top member '%s' borrowed '$s'", member["id"], member["total_borrows"])
    return {
        "member_id": member["id"],
        "borrowed": member["total_borrows"]
    }

