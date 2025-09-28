from fastapi import APIRouter, Depends, HTTPException

from app import security
from app.role.role_data_service import RoleActions
from app.role.schema import AssignPermission, CreatePermission

router = APIRouter(prefix='/role', tags=['Roles'])


@router.post('/create_permission')
async def create_permission(data: CreatePermission, current_user=Depends(security.get_current_user)):
    role = RoleActions().get_role(current_user.id)
    if role != 'admin':
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для использования данной функции.')
    RoleActions().create_permission(data)
    return {'message': 'Разрешение успешно создано'}


@router.post('/assign_permission')
async def assign_permission(data: AssignPermission, current_user=Depends(security.get_current_user)):
    role = RoleActions().get_role(current_user.id)
    if role != 'admin':
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для использования данной функции.')
    RoleActions().assign_permission(data.permission_code, data.role_code)
    return {'message': 'Разрешение успешно прикреплено к роли'}


@router.get('/all')
async def get_all_permissions(current_user=Depends(security.get_current_user)):
    role = RoleActions().get_role(current_user.id)
    if role != 'admin':
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для использования данной функции.')
    return {'message': RoleActions().get_all_permissions()}
