from logs.logger_config import logger
from database.book_db import books_db
from database.member_db import member_db, Member
from fastapi import APIRouter, HTTPException


router_report = APIRouter()

@router_report.get("/summary")
def summary():
    logger.info("Start... summary reports")
    return {
        "total_books": books_db.count_total_books(),
        "available_books": books_db.count_available_books(),
        "currently_borrowed": books_db.count_borrowed_book(),
        "active_members": member_db.count_active_members()
    }

