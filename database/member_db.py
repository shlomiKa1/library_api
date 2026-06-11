from .db_connection import db
from logs.logger_config import logger
from pydantic import BaseModel, Field
from enum import Enum


class MemberDB:
    def __init__(self):
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor()

    def craete_member(self, data):
        pass
    
    def close(self):
        self.conn.close()
        self.cursor.close()