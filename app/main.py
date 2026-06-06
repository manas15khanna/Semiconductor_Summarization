import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.init_db import init_database
from app.routes import api, pages


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(
    title="Summarization and Decision Traceability System",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    init_database()
