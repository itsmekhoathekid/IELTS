import random

class Controller:
    def __init__(self, database, collection_name):
        self.db = database
        self.collection_name = collection_name
    
    def get_random_documents(self, count=5):
        if not self.db.collection_exist(self.collection_name):
            raise ValueError(f"Collection '{self.collection_name}' does not exist in database '{self.db.db_name}'.")
        
        documents = self.db.find_documents(self.collection_name)
        if len(documents) < count:
            raise ValueError(f"Not enough documents in collection '{self.collection_name}' to return {count} random documents.")
        
        indices = random.sample(range(len(documents)), count)
        print(f"Selected indices for random documents: {indices}")
        return [documents[i] for i in indices], indices

    
    
    def mutiple_questions(self, count = 5):
        """
            return a format 
            {
                "word" : "word1",
                "options" : [
                    "meaning1",
                    "meaning2",
                    "meaning3",
                    "meaning4"
                ],
                "correct_ans" : "meaning1"
                }
        """
        result = []
        documents, selected_indices = self.get_random_documents(count)
        
        unselected_indices = set(range(len(documents))) - set(selected_indices)
        unselected_documents = [documents[i] for i in unselected_indices]

        for doc in documents:
            options = [doc['definition']]
            while len(options) < 4:
                random_doc = random.choice(unselected_documents)
                if random_doc['definition'] not in options:
                    options.append(random_doc['definition'])
            random.shuffle(options)
            result.append({
                "word": doc['word'],
                "options": options,
                "correct_ans": doc['definition']
            })

        return result
        
    