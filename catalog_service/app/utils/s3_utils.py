from loguru import logger
from aiobotocore.session import get_session

'''
For Asynchronous Events
'''
class S3Utils(object):

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    def get_object_url(self, bucket, key):
        url = f'https://{bucket}.s3.{self.region}.amazonaws.com/{key}'
        return url

    async def upload_fileobj(self, bucket, key, fileobject, expire=3600):
        session = get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(Bucket=bucket, Key=key, Body=fileobject)

            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
                presigned_url = await client.generate_presigned_url('get_object',
                    Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expire)
                return presigned_url

    async def copy_file(self, source_bucket, source_key, dest_key, dest_bucket=None):
        session = get_session()
        async with session.create_client('s3', region_name=self.region,
                                         aws_secret_access_key=self.aws_secret_access_key,
                                         aws_access_key_id=self.aws_access_key_id) as client:
            dest_bucket = source_bucket if dest_bucket is None else dest_bucket
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            await client.copy_object(Bucket=dest_bucket, CopySource=copy_source, Key=dest_key)
