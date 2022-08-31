# from loguru import logger
from fastapi import FastAPI

from app.api import catalogs
from app.core.config import settings

from app.db.mongodb import connect_to_database, close_mongo_connection
from app.core.events import create_start_app_handler, create_stop_app_handler

# def create_application() -> FastAPI:
#     application = FastAPI(
#         openapi_url="/catalogs/openapi.json",
#         docs_url="/catalogs/docs"
#         )
#     application.include_router(
#         catalogs.router,
#         tags=["catalogs"])
#     return application


# app = create_application()

# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up...")
#     await connect_to_database()


# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Shutting down...")
#     await close_mongo_connection()


def create_application() -> FastAPI:
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=settings.allowed_hosts,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(),
    )

    # application.add_exception_handler(HTTPException, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(
        catalogs.router,
        tags=["catalogs"])
    # application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = create_application()
