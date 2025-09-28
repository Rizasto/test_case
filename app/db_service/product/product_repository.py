from dataclasses import dataclass

from app.product.schema import ProductUpdate


@dataclass
class MockProduct:
    product_name: str
    price: int
    stashed: int
    measurement: str
    ad_owner: str


products: dict[int, MockProduct] = {1: MockProduct(product_name='Яблоко',
                                                   price=135,
                                                   stashed=100,
                                                   measurement='килограмм',
                                                   ad_owner='Rizasto@gmail.com'),
                                    2: MockProduct(product_name='Виноград',
                                                   price=200,
                                                   stashed=5,
                                                   measurement='килограмм',
                                                   ad_owner='Rizasto@gmail.com')}


class ProductRepository:

    @staticmethod
    def get_all_products() -> dict:
        return products

    @staticmethod
    def get_user_products(user_email: str) -> list:
        return [product for product in products.values() if
                product.ad_owner and product.ad_owner.lower() == user_email]

    @staticmethod
    def update_product(data: ProductUpdate, user_email: str, permission_type: str) -> None:
        product_name = data.product_name if data.product_name else None
        price = data.price if data.price else None
        stashed = data.stashed if data.stashed else None
        measurement = data.measurement if data.measurement else None
        for item, value in products.items():
            if item == data.id and permission_type == 'all' or item == data.id and value.ad_owner.lower() == user_email:
                product = products.get(item)
                product.product_name = product_name if product_name else product.product_name
                product.price = price if price else product.price
                product.stashed = stashed if stashed else product.stashed
                product.measurement = measurement if measurement else product.measurement
                break
