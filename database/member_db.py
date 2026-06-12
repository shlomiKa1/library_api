from .db_connection import db
from logs.logger_config import logger
from pydantic import BaseModel, Field, EmailStr
from config import COUNT_BOOKS

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
    
    def deactivate_member(self, member_id: int) -> bool:
        logger.info("Start... deactivate member by ID '%s' on database", member_id)

        self.cursor.execute(
            "UPDATE members SET is_active = FALSE WHERE id = %s",
            (member_id, )    
        )
        self.conn.commit()
        deactivated = self.cursor.rowcount > 0
        self.close()

        return deactivated
    
    def activate_member(self, member_id: int) -> bool:
        logger.info("Start... activate member by ID '%s' on database", member_id)

        self.cursor.execute(
            "UPDATE members SET is_active = True Where id = %s",
            (member_id,)
        )
        self.conn.commit()
        activated = self.cursor.rowcount > 0
        self.close()

        return activated
    
    def increment_borrows(self, member_id: int) -> bool:
        logger.info("Start... count how many books member by ID '%s' borrow on database")
        
        self.cursor.execute("SELECT total_borrows FROM members WHERE id = %s", (member_id,))
        total = self.cursor.fetchone()


        if total < COUNT_BOOKS:
            total += 1
            self.cursor.execute("UPDATE members SET total_borrows = %s", (total,))
            self.conn.commit()

        if total == COUNT_BOOKS:
            logger.warning("Member ID '%s' come to is limit - %s", member_id, total)

        increment = self.cursor.rowcount > 0
        self.close()

        return increment
    
    def close(self) -> None:
        self.cursor.close()
        self.conn.close()