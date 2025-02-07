from passlib.context import CryptContext

from app.src.api.infraestructure.repositories.user_repository import UserRepository
from app.src.api.domain.schemas.user_schema import UserCreateRequest
from app.src.api.exceptions.custom_exceptions import NotFoundError

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserService:
    '''
    Servicio para manejar la lógica de negocio relacionada con usuarios.
    '''
    
    def __init__(self):
        self.repository = UserRepository()

    def hash_password(self, password: str) -> str:
        '''
        Genera un hash seguro de la contraseña usando bcrypt.
        '''
        return pwd_context.hash(password)

    async def create_user(self, user: UserCreateRequest) -> dict:
        '''
        Crea un nuevo usuario verificando que el email no exista.
        Hashea la contraseña antes de almacenarla.
        '''
        if await self.repository.get_user_by_email(user.email):
            raise NotFoundError(message='Email ya registrado.')
        
        user_dict = user.model_dump()
        user_dict['password'] = self.hash_password(user_dict['password'])
        
        return await self.repository.create_user(user_dict)
