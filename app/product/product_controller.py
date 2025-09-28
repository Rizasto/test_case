from fastapi import APIRouter, Depends, HTTPException

from app import security
from app.product.product_service import ProductActions
from app.product.schema import ProductUpdate
from app.role.role_data_service import RoleActions

router = APIRouter(prefix='/product', tags=['Products'])


@router.get('')
async def get_all_products(current_user=Depends(security.get_current_user)):
    permission = RoleActions().check_permission('get_all_products', current_user.id)
    if not permission:
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для просмотра данного раздела.')
    return {'message': ProductActions().get_all_products()}


@router.get('/my')
async def get_user_products(current_user=Depends(security.get_current_user)):
    permission = RoleActions().check_permission('get_my_products', current_user.id)
    if not permission:
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для просмотра данного раздела.')
    return {'message': ProductActions().get_user_products(current_user.email)}


@router.patch('/update_product')
async def update_product(data: ProductUpdate, current_user=Depends(security.get_current_user)):
    my_permission = RoleActions().check_permission('update_my_products', current_user.id)
    all_permission = RoleActions().check_permission('update_all_products', current_user.id)
    permission_type = 'all' if all_permission else 'my'
    if not my_permission or not all_permission:
        raise HTTPException(status_code=403, detail='У Вас недостаточно прав для просмотра данного раздела.')
    ProductActions().update_product(data, current_user.email, permission_type)
    return {'message': 'Данные успешно обновлены'}

