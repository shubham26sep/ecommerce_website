from loguru import logger
from bson import ObjectId
from app.services import DBSessionContext
from app.db.mongodb import get_database
from app.models.category import CategoryModel


class CategoryService:

    async def create_category(self, category_data):
        category_data = await self.prepare_category_data(category_data)
        category_id = await CategoryCRUD().create(category_data)
        category = await CategoryCRUD().get(category_id)
        category_response = CategoryModel(**category)
        return category_response

    async def update_category(self, category_id, category_data):
        logger.info(category_data)
        category_data = await self.prepare_category_data(category_data)
        category = await CategoryCRUD().get(category_id)

        updated_fields = []
        for field in ('name', 'parent'):
            if category_data[field] != category[field]:
                updated_fields.append(field)
        
        if updated_fields:
            await CategoryCRUD().update(category_id, category_data)

        category_data.update({'_id': ObjectId(category_id)})
        category_response = CategoryModel(**category_data)
        return category_response

    async def prepare_category_data(self, category_data):
        if 'parent' not in category_data or category_data['parent'] is None:
            category_data['level'] = 0
            category_data['parent'] = '/'
            category_data['path'] = f"/{category_data['name']}"
        else:
            parent_category_id = category_data['parent']
            parent_category = await CategoryCRUD().get(parent_category_id)
            if parent_category is None:
                raise Exception('Invalid parent category id')
            category_data['level'] = parent_category['level'] + 1
            if category_data['level'] == 1:
                category_data['parent'] = f"/{parent_category['name']}"
            else:
                category_data['parent'] = f"{parent_category['parent']}/{parent_category['name']}"
            category_data['path'] =  f"{parent_category['path']}/{category_data['name']}"
        return category_data


class CategoryCRUD(DBSessionContext):

    COLLECTION_NAME = 'Category'

    def __init__(self):
        super().__init__(get_database())

    async def create(self, category_data):
        category = await self.db[CategoryCRUD.COLLECTION_NAME].insert_one(category_data)
        return category.inserted_id

    async def update(self, category_id, category_data):
        await self.db[CategoryCRUD.COLLECTION_NAME].replace_one({"_id": ObjectId(category_id)}, category_data)
        return True

    async def get(self, category_id):
        category = await self.db[CategoryCRUD.COLLECTION_NAME].find_one({'_id': ObjectId(category_id)})
        return category

    async def filter(self, query_filter):
        sub_categories = await self.db[CategoryCRUD.COLLECTION_NAME].find(query_filter)
        return sub_categories
