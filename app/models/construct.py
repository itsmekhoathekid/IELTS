from pymongo import MongoClient


class Construct:
    def __init__(self, text_file, connect_string, collection_name, db_name):
        self.text_file = text_file
        self.client = MongoClient(connect_string)
        self.collection_name = collection_name
        self.db_name = db_name
    
    def remove_whitespace(self, sentence):
        return ' '.join(sentence.split())

    def collection_exist(self):
        db = self.client[self.db_name]
        return self.collection_name in db.list_collection_names()

    def check_format(self, sentence):
        if ':' not in sentence:
            raise ValueError("Sentence does not contain a colon.")
        if len(sentence.split(':')) != 2:
            raise ValueError("Sentence should contain exactly one colon.")
        if '_' not in sentence.split(':')[0]:
            raise ValueError("Word part of the sentence does not contain the type of that word.")
        return True
    
    def process(self, sentence):
        word = sentence.split(':')[0].split('_')[0]
        definition = sentence.split(':')[1].strip()
        types = sentence.split(':')[0].split('_')[1:]
        return {
            'word': self.remove_whitespace(word),
            'definition': self.remove_whitespace(definition),
            'types': [self.remove_whitespace(t) for t in types]
        }


    def push_into_database(self):
        if not self.collection_exist():
            db = self.client[self.db_name]
            collection = db[self.collection_name]
        else:
            collection = self.client[self.db_name][self.collection_name]

        with open(self.text_file, 'r') as file:
            for line in file:
                line = line.strip()
                data_line = self.process(line)
                collection.insert_one(data_line)
        print(f"Data pushed into collection '{self.collection_name}' in database '{self.db_name}'.")

    def print_collection(self):
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        print(f"Documents in collection '{self.collection_name}':")
        for doc in collection.find():
            print(doc)