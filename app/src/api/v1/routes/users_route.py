from fastapi import APIRouter

from app.src.api.services.user_service import UserService
from app.src.api.domain.schemas.user_schema import UserCreateRequest
from app.src.api.domain.schemas.user_schema import UserCreateResponse

# Router from api.
router = APIRouter(prefix='/users',
                   tags=['Users'])

@router.post('/sing-up/', response_model=UserCreateResponse)
async def create_user(user: UserCreateRequest):
    '''
    Endpoint para registrar un nuevo usuario.
    '''
    service = UserService()
    return await service.create_user(user=user)
