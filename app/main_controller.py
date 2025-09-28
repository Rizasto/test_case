from fastapi import FastAPI

from app.product.product_controller import router as product_router
from app.role.role_data_controller import router as role_router
from app.user_data.user_data_controller import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(role_router)
