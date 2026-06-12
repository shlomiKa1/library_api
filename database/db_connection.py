from logs.logger_config import logger
from secret_details import CONMNECTION, DATABASE
import mysql.connector


class DbConn:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

        self.conn = self.get_connect()

    def get_connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

    def get_connection(self):
        if self.conn.is_connected():
            return self.conn
        
        self.conn = self.get_connect()
        return self.conn

    def create_database(self):
        cursor = self.conn.cursor()

        # Its ok to put f-string for a database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        logger.info("Database '%s' created successfully", DATABASE)
        self.conn.commit()

        cursor.execute(f"USE {DATABASE}")
        
        cursor.close()

    def create_table_books(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS books(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(50) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    genre ENUM("Fiction", "Non-Fiction", "Science", "History", "Other"),
                    is_available BOOLEAN DEFAULT TRUE,
                    borrowed_by_member_id INT DEFAULT NULL
                )
            """
        )
        self.conn.commit()
        logger.info("Books table created successfully")
        
        cursor.close()

    def create_table_members(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS members(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(30) UNIQUE,
                    is_active BOOLEAN DEFAULT TRUE,
                    total_borrows INT DEFAULT NULL
                )
            """
        )
        self.conn.commit()
        logger.info("Members table created successfully")

        cursor.close()

db = DbConn(CONMNECTION["host"], CONMNECTION["user"], CONMNECTION["password"])
print(CONMNECTION["user"])