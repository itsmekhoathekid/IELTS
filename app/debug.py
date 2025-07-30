import streamlit as st
import pandas as pd
from models import Controller, Database
import random

# Kết nối MongoDB
connect_string = 'mongodb://localhost:27017/'
db_name = 'vocab_app'
collection_name = 'dictionary'

database = Database(connect_string, db_name)
controller = Controller(database, collection_name)


print("Num lines: ", database.get_num_line(collection_name))