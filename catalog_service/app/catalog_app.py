# from loguru import logger
from fastapi import FastAPI

from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from app.api import category, products
from app.core.config import settings
from app.core.errors import http_error_handler, http_422_error_handler
from app.core.events import create_start_app_handler, create_stop_app_handler

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

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http_422_error_handler)
    application.include_router(
        category.router,
        tags=["categories"])
    application.include_router(
        products.router,
        tags=["products"])
    # application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = create_application()
