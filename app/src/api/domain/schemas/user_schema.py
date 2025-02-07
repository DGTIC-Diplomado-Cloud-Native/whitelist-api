import re

from pydantic import BaseModel, Field, field_validator
from app.src.api.exceptions.custom_exceptions import ValidationError

class UserCreateRequest(BaseModel):
    '''
    Modelo Pydantic para validar los datos de registro de usuario.
    '''
    
    email: str = Field(..., description='Email del usuario.')
    phone: str = Field(..., description='Celular del usuario.')
    password: str = Field(..., description='Password del usuario.')
    
    class Config:
        from_attributes = True
        populate_by_name = True
        
    @field_validator('email')
    def validate_email(cls, v):
        '''
        Valida el formato del email usando regex.
        '''
        if v is not None:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if bool(re.match(pattern, v)):
                return v
            else:
                raise ValidationError('El email no es válido.')
            
    @field_validator('phone')
    def validate_phone(cls, v):
        '''
        Valida el formato del teléfono usando regex. 
        Debe tener 10-15 dígitos con prefijo + opcional.
        '''
        if v is not None:
            pattern = r'^\+?[1-9]\d{9,14}$'
            if bool(re.match(pattern, v)):
                return v
            else:
                raise ValidationError('El teléfono no es válido.')
            
    @field_validator('password')
    def validate_password(cls, v):
        '''
        Valida la fortaleza de la contraseña.
        Requisitos:
        - Mínimo 8 caracteres
        - Al menos 1 mayúscula
        - Al menos 1 minúscula
        - Al menos 1 número 
        - Al menos 1 carácter especial
        '''
        if v is not None:
            if len(v) < 8:
                return False
            
            has_upper = any(c.isupper() for c in v)
            has_lower = any(c.islower() for c in v)
            has_digit = any(c.isdigit() for c in v)
            has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v)
            
            if has_upper and has_lower and has_digit and has_special:
                return v
            else: 
                raise ValidationError('El teléfono no es válido.')
            
class UserCreateResponse(BaseModel):
    '''
    Modelo Pydantic para la respuesta del registro de usuario. 
    Contiene los datos del usuario creado en MongoDB.
    '''
    id: str = Field(..., description='Id del usuario en MongoDB.')
    email: str = Field(..., description='Email del usuario.')
    phone: int = Field(..., description='Celular del usuario.')
    
    class Config:
        from_attributes = True
        populate_by_name = True
