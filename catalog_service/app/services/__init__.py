from app.core.config import get_app_settings

class DBSessionContext(object):
    def __init__(self, db):
        self.db = db
        self.config = get_app_settings()
    
    # def create_session(self):
    #     return self.db.client.start_session(causal_consistency=False)

    # def end_session(self, s):
    #     return s.end_session()

# class AppService(object):
#     def __init__(self):
#         self.config = config
        
#     def notify_sync_event(self):
#         pass


# class AppCRUD(DBSessionContext):
#     pass