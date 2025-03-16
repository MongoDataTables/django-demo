from pymongo import MongoClient


class MongoConnection:
    def __init__(self, host='localhost', port=27017, db_name='book_database'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]


class MongoCollection:
    def __init__(self, collection_name, connection=None):
        self.collection_name = collection_name
        self.connection = connection or MongoConnection()
        self.collection = self.connection.db[collection_name]
    
    def find(self, query=None, projection=None):
        query = query or {}
        return list(self.collection.find(query, projection))
    
    def count(self, query=None):
        query = query or {}
        return self.collection.count_documents(query)
    
    def get_keys(self):
        keys = set()
        for doc in self.collection.find({}, {'_id': 0}):
            keys.update(doc.keys())
        return sorted(list(keys))
