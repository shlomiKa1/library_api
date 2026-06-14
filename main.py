from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from routes.book_routes import router_books
from routes.member_routes import router_members
from routes.report_routes import router_report
from contextlib import asynccontextmanager
from database.db_connection import db


@asynccontextmanager
async def lifespan(app: FastAPI):  
    yield

    db.conn.close()

app = FastAPI(lifespan=lifespan)

# exception_handlers(HTTPException)
def http_exception(rew: Request, e: HTTPException):
    return JSONResponse(
        content="",
        status_code=400
    )

app.include_router(router=router_books, prefix="/books")
app.include_router(router=router_members, prefix="/members")
app.include_router(router=router_report, prefix="/reports")