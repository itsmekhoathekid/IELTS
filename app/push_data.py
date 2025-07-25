from utils import (
    read_text
)

from models import (
    Construct
)

text_string = '/home/anhkhoa/IELTS/data/texts/test.txt'
connect_string = 'mongodb://localhost:27017/'
collection_name = 'dictionary'
db_name = 'vocab_app'

controller = Construct(text_string, connect_string, collection_name, db_name)
controller.push_into_database()
controller.print_collection()
controller.client.close()