from logs.logger_config import logger
from secret_details import CONMNECTION, DATABASE
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=CONMNECTION["host"],
        user=CONMNECTION["user"],
        password=CONMNECTION["password"]
    )

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS %s", (DATABASE,))
    logger.info("Database '%s' created successfully", DATABASE)
    conn.commit()
    
    cursor.close()
    conn.close()

def create_table_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS books(
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                author VARCHAR(50) NOT NULL,
                genre ENUM(Fiction, Non-Fiction, Science, History, Other),
                is_available BOOLEAN DEFUALT TRUE,
                borrowed_by_member_id INT DEFUALT NULL
            )
        """
    )
    conn.commit()
    logger.info("Books table created successfully")
    
    cursor.close()
    conn.close()

def create_table_members():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS members(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(30) UNIQUE,
                is_active BOOLEAN DEFUALT TRUE,
                total_borrows INT DEFUALT NULL
            )
        """
    )
    conn.commit()
    logger.info("Members table created successfully")

    cursor.close()
    conn.close()