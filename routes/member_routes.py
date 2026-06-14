from logs.logger_config import logger
from database.book_db import books_db
from database.member_db import member_db, Member
from fastapi import APIRouter, HTTPException

router_members = APIRouter()

@router_members.post("", status_code=201)
def add_member(new_member: Member):
    logger.info("Start... add a new member - server")

    new_id = member_db.craete_member(new_member)

    if not new_id:
        raise HTTPException(500, "Internal Server Error")
    return {"Message": f"Meber created successfully is ID '{new_id}'"}
    
@router_members.get("", status_code=200)
def get_members():
    logger.info("Start... get all members - server")

    members = member_db.get_all_members()
    logger.info("Return '%s' members", len(members))

    return {"Message": members}
