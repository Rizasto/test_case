from fastapi import APIRouter, Depends, HTTPException

from app import security
from app.user_data.schema import LogIn, TokenOut, UserAdd, UserUpdate
from app.user_data.user_data_service import UserAction
from config import JWT_SETTINGS

router = APIRouter(prefix='/user', tags=['User'])


@router.post('/register')
async def register_user(user: UserAdd):
    if user.password != user.password_repeat:
        return {'message': 'Пароли не совпадают'}
    registered_user = UserAction().register_user(user)
    if registered_user:
        return {'message': 'Пользователь успешно зарегистрирован!'}
    return {'message': f'Пользователь с email: {user.email} уже существует.'}


@router.post('/login', response_model=TokenOut)
async def login(data: LogIn):
    user = UserAction().get_user_by_email(data.email.lower())
    if not user or not getattr(user, 'is_active', False):
        raise HTTPException(status_code=401, detail='Неверные данные')
    if not UserAction.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Неверные данные')
    access = security.issue_access(user_id=user.id)
    return TokenOut(access_token=access, expires_in=int(JWT_SETTINGS['access_ttl_min']) + 15)


@router.post('/logout')
async def logout(token: str = Depends(security.get_bearer_token)):
    payload = security.decode_access(token)
    jti = payload['jti']
    exp = int(payload['exp'])
    security.revoked_access[jti] = exp
    return {'message': 'logout успешен'}


@router.patch('/update')
async def update_info(data: UserUpdate = Depends(), current_user=Depends(security.get_current_user)):
    UserAction().update_info(current_user.id, data)
    return {'message': 'Данные обновлены'}


@router.delete('/delete')
async def delete_user(current_user=Depends(security.get_current_user)):
    router.get('/logout')
    UserAction().delete_user(current_user.id)
    return {'message': f'Пользователь {current_user.email} удален'}
