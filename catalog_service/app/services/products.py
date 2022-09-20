from loguru import logger
from bson import ObjectId
from collections import defaultdict
from app.services import DBSessionContext
from app.db.mongodb import get_database
from app.models.products import ProductModel
from app.services.category import CategoryCRUD
from app.services.images import ImageService


class ProductService:

    async def create_product(self, product_data):
        product_data = await self.prepare_product_data(product_data)
        product_id = await ProductCRUD().create(product_data)
        product = await ProductCRUD().get(product_id)
        product_response = ProductModel(**product)
        return product_response

    def get_category_levels(self, category):
        path, level = category['path'], category['level']
        path = path.split('/')
        categories = defaultdict(list)
        for i in range(level+1):
            categories[f'level{i}'].append('/'.join(path[:i+1]))
        return categories

    async def upload_images(self, images):
        image_service = ImageService()
        images = [await image_service.copy_image_from_presigned_url(image['image_url']) for image in images]
        return images
            
    async def prepare_product_data(self, product_data):
        category_id = product_data.pop('category_id')
        category = await CategoryCRUD().get(category_id)
        product_data['categories'] = self.get_category_levels(category)
        product_data['prices'] = {'price': product_data['price'], 'special_price': ''}
        product_data['images'] = await self.upload_images(product_data['images'])
        return product_data


class ProductCRUD(DBSessionContext):

    COLLECTION_NAME = 'Products'

    def __init__(self):
        super().__init__(get_database())

    async def create(self, product_data):
        product = await self.db[ProductCRUD.COLLECTION_NAME].insert_one(product_data)
        return product.inserted_id

    async def update(self, product_id, product_data):
        await self.db[ProductCRUD.COLLECTION_NAME].replace_one({"_id": ObjectId(product_id)}, product_data)
        return True

    async def get(self, product_id):
        product = await self.db[ProductCRUD.COLLECTION_NAME].find_one({'_id': ObjectId(product_id)})
        return product

    async def list(self, query_filter=None):
        if query_filter is None:
            cursor = self.db[ProductCRUD.COLLECTION_NAME].find()
        else:
            cursor = self.db[ProductCRUD.COLLECTION_NAME].find(query_filter)
        products = [product async for product in cursor]
        return products
