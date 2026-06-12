from .db_connection import db
from logs.logger_config import logger
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Member(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr

class MemberDB:
    def __init__(self):
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def craete_member(self, data: Member) -> int | None:
        logger.info("Start... Create a member on database")

        self.cursor.execute(
            "INSERT INTO members (name, email) VALUES(%s, %s)",
            (data.name, data.email)    
        )
        self.conn.commit()
        new_id = self.cursor.lastrowid
        self.close()

        return new_id
    
    def get_all_members(self) -> list[dict]:
        logger.info("Start... Get all members from database")

        self.cursor.execute("SELECT * FROM members")
        rows = self.cursor.fetchall()
        self.close()

        return rows
    
    def get_member_by_id(self, member_id: int) -> dict | None:
        logger.info("Start... Get member by ID '%s' from database", member_id)

        self.cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
        row = self.cursor.fetchone()
        self.close()

        return row
    
    def update_member(self, member_id: int, data: Member) -> bool:
        logger.info("Start... update member by ID '%s' on database", member_id)

        data = data.model_dump(exclude_unset=True)
        parts = [f"{key} = %s" for key in data.keys()]
        join_parts = ", ".join(parts)

        self.cursor.execute(
            "UPDATE members SET (%s) WHERE id = %s",
            (join_parts, list(data.values()) + [member_id])
        )
        self.conn.commit()
        updated = self.cursor.rowcount > 0
        self.close()

        return updated

    def close(self):
        self.cursor.close()
        self.conn.close()