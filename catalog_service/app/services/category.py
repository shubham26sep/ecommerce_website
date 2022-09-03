from app.services import DBSessionContext
from app.db.mongodb import get_database

class CategoryCRUD(DBSessionContext):

    COLLECTION_NAME = 'Category'

    def __init__(self):
        super().__init__(get_database())

    async def create(self, category_data):
        response = await self.db[CategoryCRUD.COLLECTION_NAME].insert_one(category_data)
        return response
