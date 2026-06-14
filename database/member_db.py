from .db_connection import db
from logs.logger_config import logger
from pydantic import BaseModel, Field, EmailStr


class Member(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr

class MemberDB:
    def __init__(self):
        self.conn = db.conn

    def craete_member(self, data: Member) -> int | None:
        data = data.model_dump()
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO members (name, email) VALUES(%s, %s)",
                (data["name"], data["email"])    
            )
            self.conn.commit()
            logger.info("Add a new member on database")
            return cursor.lastrowid
    
    def get_all_members(self) -> list[dict]:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()

    def get_member_by_id(self, member_id: int) -> dict | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            return cursor.fetchone()
    
    def update_member(self, member_id: int, data: dict) -> bool:
        parts = [f"{key} = %s" for key in data.keys()]
        join_parts = ", ".join(parts)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                f"UPDATE members SET {join_parts} WHERE id = %s",
                list(data.values()) + [member_id]
            )
            self.conn.commit()
            logger.info("Member ID '%s' is updated", member_id)
            return cursor.rowcount > 0
    
    def deactivate_member(self, member_id: int) -> bool:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET is_active = FALSE WHERE id = %s",
                (member_id,)    
            )
            self.conn.commit()
            logger.info("deactivate member ID '%s' on database", member_id)
            return cursor.rowcount > 0

    def activate_member(self, member_id: int) -> bool:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET is_active = True Where id = %s",
                (member_id,)
            )
            self.conn.commit()
            logger.info("Activate member ID '%s' on database", member_id)
            return cursor.rowcount > 0
        
    def increment_borrows(self, member_id: int) -> bool:        
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE members SET total_borrows = COALESCE(total_borrows, 0) +1 WHERE id = %s", (member_id,))
            self.conn.commit()
            logger.info("Count books that member ID '%s' borrow on database", member_id)
            return cursor.rowcount > 0
        
    def count_active_members(self) -> int | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(name) FROM members WHERE is_active = TRUE")
            return cursor.fetchone()["COUNT(name)"]
    
    def get_top_member(self) -> dict | None:
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                    SELECT id as member_id , total_borrows as borrowed FROM members
                    WHERE total_borrows = (SELECT MAX(total_borrows) FROM members)

                """
            )
            return cursor.fetchall()
        

member_db = MemberDB()