from logs.logger_config import logger
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
        raise HTTPException(404, "Member not found")
    
    logger.info("Return member by ID '%s'", id)
    return {"Message": member}

@router_members.patch("/{id}", status_code=200)
def edit_member(id: int, new_member: Member):
    logger.info("Start... update member by ID '%s' - server", id)

    member_by_id(id)
    member_db.update_member(id, new_member.model_dump(exclude_unset=True))
    
    logger.info("Updated member ID '%s' successfully", id)
    return {"Message": f"Updated member ID {id} successfully"}

@router_members.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logger.info("Start... dactivate member by ID '%s' - server", id)

    member_by_id(id)
    member_db.deactivate_member(id)

    logger.info("Deactivated member by ID '%s'", id)
    return {"Message": f"Deactivated member by ID {id}"}

@router_members.patch("/{id}/activate")
def activate_member(id: int):
    logger.info("Start... activate member by ID '%s' - Server", id)

    member_by_id(id)
    member_db.activate_member(id)
    
    logger.info("Activate member by ID '%s'", id)
    return {"Message": f"Activated member ID '{id}'"}