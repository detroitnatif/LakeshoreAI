from deta import Deta
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

deta_key = os.getenv('DETA_API_KEY')


deta = Deta(deta_key)
db = deta.Base('users_db')

def insert_user(username, name, password):
    '''Returns the user on a sucessful user creation, otherwise raises an error'''
    return db.put({'key': username, 'name': name, 'password': password})

insert_user('tklimas', 'ty klimas', '1234')

