import os
from datetime import datetime
from loguru import logger

from app.utils.s3_utils import S3Utils
from app.core.config import settings


class ImageService:

    VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png')

    def __init__(self):
        self.s3_utils = S3Utils(settings.aws_access_key_id,
                                settings.aws_secret_access_key,
                                settings.aws_region)
        self.bucket = settings.s3_image_bucket
        self.prefix = 'products/'

    async def upload_image(self, file_obj):
        filename = file_obj.filename
        _, extension = os.path.splitext(filename)
        if extension not in ImageService.VALID_EXTENSIONS:
            raise Exception(f'Invalid extension {extension}')
    
        data = file_obj.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
        presigned_url = await self.s3_utils.upload_fileobj(
            self.bucket, 
            self.prefix + filename,
            data)
        return presigned_url
