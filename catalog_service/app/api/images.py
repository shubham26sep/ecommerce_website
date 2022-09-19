from loguru import logger
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.exceptions import HTTPException

from starlette.responses import JSONResponse
from app.models import SuccessResponseSchema, ErrorResponseSchema
from app.core.errors import custom_error_message
from app.services.images import ImageService

router = APIRouter(prefix="/catalogs/images")


@router.post(
    "/upload_image", response_model=SuccessResponseSchema
)
async def upload_image(
    file: UploadFile,
    ):
    logger.info(file)
    try:
        image_url = await ImageService().upload_image(file)
        if image_url is None:
            return custom_error_message(jsonable_encoder(ErrorResponseSchema(
                statusCode=400, message='Unable to upload file'))
            )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                detail=jsonable_encoder(ErrorResponseSchema(statusCode=400, message = str(e))))
    return SuccessResponseSchema(data={'image_url': image_url})
