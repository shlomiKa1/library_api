from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routes.book_routes import router_books
from routes.member_routes import router_members
from routes.report_routes import router_report
from contextlib import asynccontextmanager
from database.db_connection import db
from logs.logger_config import logger
import mysql.connector


@asynccontextmanager
async def lifespan(app: FastAPI):  
    yield

    db.conn.close()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def exception_request_(req: Request, e: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content= {
            "detail": "Invalid input",
            "error": e.errors()
        }
    )
@app.exception_handler(HTTPException)
def http_exception(rew: Request, e: HTTPException):
    logger.error(e)
    return JSONResponse(
        content={"detail": e}
    )
@app.exception_handler(mysql.connector.Error)
def mysql_exception(req: Request, e: mysql.connector.Error):
    logger.error(e)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

app.include_router(router=router_books, prefix="/books")
app.include_router(router=router_members, prefix="/members")
app.include_router(router=router_report, prefix="/reports")