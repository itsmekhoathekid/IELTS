from utils import (
    read_text
)

from models import (
    Construct,
    Database
)

text_string = '/home/anhkhoa/IELTS/data/texts/test.txt'
connect_string = 'mongodb://localhost:27017/'
collection_name = 'dictionary'
db_name = 'vocab_app'

database = Database(connect_string, db_name)
controller = Construct(text_string, database, collection_name)
controller.push_into_database()
controller.print_collection()