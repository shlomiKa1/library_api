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

    def craete_member(self, data: Member) -> int | None:
        logger.info("Start... Create a member on database")

        data = data.model_dump()
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO members (name, email) VALUES(%s, %s)",
                (data["name"], data["email"])    
            )
            self.conn.commit()
            return cursor.lastrowid
    
    def get_all_members(self) -> list[dict]:
        logger.info("Start... Get all members from database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()

    def get_member_by_id(self, member_id: int) -> dict | None:
        logger.info("Start... Get member by ID '%s' from database", member_id)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
            return cursor.fetchone()
    
    def update_member(self, member_id: int, data: dict) -> bool:
        logger.info("Start... update member by ID '%s' on database", member_id)

        parts = [f"{key} = %s" for key in data.keys()]
        join_parts = ", ".join(parts)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET (%s) WHERE id = %s",
                (join_parts, list(data.values()) + [member_id])
            )
            self.conn.commit()
            return cursor.rowcount > 0
    
    def deactivate_member(self, member_id: int) -> bool:
        logger.info("Start... deactivate member by ID '%s' on database", member_id)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET is_active = FALSE WHERE id = %s",
                (member_id, )    
            )
            self.conn.commit()
            return cursor.rowcount > 0

    def activate_member(self, member_id: int) -> bool:
        logger.info("Start... activate member by ID '%s' on database", member_id)

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET is_active = True Where id = %s",
                (member_id,)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        
    def increment_borrows(self, member_id: int) -> bool:
        logger.info("Start... count how many books member by ID '%s' borrow on database")
        
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT total_borrows FROM members WHERE id = %s", (member_id,))
            total = cursor.fetchone()


            if total < COUNT_BOOKS:
                total += 1
                cursor.execute("UPDATE members SET total_borrows = %s", (total,))
                self.conn.commit()

            if total == COUNT_BOOKS:
                logger.warning("Member ID '%s' come to is limit - %s", member_id, total)

            return cursor.rowcount > 0
        
    def count_active_members(self) -> int | None:
        logger.info("Start... get total of activate members on database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(name) FROM members WHERE is_active = TRUE")
            return cursor.fetchone()
    
    def get_top_member(self) -> dict | None:
        logger.info("Start... get top activate member from database")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                    SELECT *, MAX(total_borrows) as max_total
                    WHERE total_borrows = max_total
                """
            )
            return cursor.fetchone()
        

member_db = MemberDB()