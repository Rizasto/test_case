from app.product.schema import ProductUpdate
from app.db_service.product.product_repository import ProductRepository


class ProductActions:
    def __init__(self) -> None:
        self.repository = ProductRepository

    def get_all_products(self) -> dict:
        return self.repository.get_all_products()

    def get_user_products(self, user_email: str) -> list:
        return self.repository.get_user_products(user_email)

    def update_product(self, data: ProductUpdate, user_email: str, permission_type: str) -> None:
        self.repository.update_product(data, user_email, permission_type)
