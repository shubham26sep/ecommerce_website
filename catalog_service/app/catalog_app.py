from loguru import logger
from fastapi import FastAPI

from app.api import catalogs
from app.db.mongodb import connect_to_database, close_mongo_connection


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/catalogs/openapi.json",
        docs_url="/catalogs/docs"
        )
    application.include_router(
        catalogs.router,
        tags=["catalogs"])
    return application


app = create_application()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    await connect_to_database()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
    await close_mongo_connection()
