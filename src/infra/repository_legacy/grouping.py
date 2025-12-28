from infra.cache.firestore import CacheFirestoreAsync

class CacheFirestoreRepository(CacheFirestoreAsync):
    def __init__(self):
        
        super().__init__(
            collection=f"cache", 
            )