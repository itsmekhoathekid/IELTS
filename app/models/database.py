from pymongo import MongoClient

class Database:
    def __init__(self, connect_string, db_name):
        self.client = MongoClient(connect_string)
        self.db_name = db_name

    def collection_exist(self, collection_name):
        db = self.client[self.db_name]
        return collection_name in db.list_collection_names()

    def get_collection(self, collection_name):
        if not self.collection_exist(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist in database '{self.db_name}'.")
        return self.client[self.db_name][collection_name]

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        collection.insert_one(document)

    def find_documents(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        return list(collection.find(query or {}))
    
    def print_collection(self, collection_name):
        collection = self.get_collection(collection_name)
        print(f"Documents in collection '{collection_name}':")
        for doc in collection.find():
            print(doc)

    def close(self):
        self.client.close()
        print("Database connection closed.")