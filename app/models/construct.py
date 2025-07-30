from pymongo import MongoClient
from .database import Database

class Construct:
    def __init__(self, text_file, database, collection_name):
        self.text_file = text_file
        self.db = database
        self.collection_name = collection_name
    
    def remove_whitespace(self, sentence):
        return ' '.join(sentence.split())

    def collection_exist(self):
        return self.db.collection_exist(self.collection_name)

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
            raise ValueError(f"Collection '{self.collection_name}' does not exist in database '{self.db.db_name}'.")

        with open(self.text_file, 'r') as file:
            for line in file:
                line = line.strip()
                data_line = self.process(line)
                word = data_line['word']
                if word in [doc['word'] for doc in self.db.find_documents(self.collection_name, {'word': word})]:
                    print(f"Word '{word}' already exists in the collection. Skipping.")
                    continue
                else:
                    self.check_format(line)
                    print(f"Adding word '{word}' to the collection.")
                    self.db.insert_document(self.collection_name, data_line)

    def print_collection(self):
        if not self.collection_exist():
            raise ValueError(f"Collection '{self.collection_name}' does not exist in database '{self.db.db_name}'.")
        self.db.print_collection(self.collection_name)
    
    def get_num_line(self):
        if not self.collection_exist():
            raise ValueError(f"Collection '{self.collection_name}' does not exist in database '{self.db.db_name}'.")
        return self.db.get_num_line(self.collection_name)