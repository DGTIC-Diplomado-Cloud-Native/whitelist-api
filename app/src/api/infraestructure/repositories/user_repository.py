import os

from pymongo import MongoClient

from dotenv import load_dotenv

# ENV
load_dotenv()

class UserRepository:
    '''
    Repositorio para manejar operaciones CRUD de usuarios en MongoDB.
    '''
    
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client.whitelist_db
        self.collection = self.db.users

    async def create_user(self, user: dict) -> dict:
        '''
        Crea un nuevo usuario en la base de datos.
        Añade el ID generado por MongoDB al diccionario del usuario.
        '''
        result = self.collection.insert_one(user)
        user['id'] = str(result.inserted_id)
        return user

    async def get_user_by_email(self, email: str) -> dict:
        '''
        Busca un usuario por su email en la base de datos.
        '''
        return self.collection.find_one({'email': email})
