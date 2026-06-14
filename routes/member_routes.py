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

@router_members.get("/{id}", status_code=200)
def member_by_id(id: int):
    logger.info("Start... get member by ID '%s' - server", id)

    member = member_db.get_member_by_id(id)
    if not member:
        raise HTTPException(404, "ID not found")
    
    logger.info("Return member by ID '%s'", id)
    return {"Message": member}

@router_members.patch("/{id}", status_code=200)
def edit_member(id: int, new_member: Member):
    logger.info("Start... update member by ID '%s' - server", id)

    updated = member_db.update_member(id, new_member.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(404, "ID not found")
    
    logger.info("Updated member ID '%s' successfully", id)
    return {"Message": f"Updated member ID {id} successfully"}

@router_members.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logger.info("Start... dactivate member by ID '%s' - server", id)

    deactivated = member_db.deactivate_member(id)
    if not deactivated:
        raise HTTPException(404, "ID not found")

    logger.info("Deactivated member by ID '%s'", id)
    return {"Message": f"Deactivated member by ID {id}"}
