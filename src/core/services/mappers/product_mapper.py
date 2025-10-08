
from core.models import Product
from core.schemas.product import ProductRead, ProductCreate


def model_to_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        article=product.article,
        name=product.name,
        description=product.description,
        author=product.author.name,
        price=product.price,
        discount_price=product.discount_price,
        stock_quantity=product.stock_quantity,
        image=product.image,
        minimal_age=product.minimal_age,
        is_active=product.is_active
    )

def create_to_model(product_create: ProductCreate, article: str, author_id: int) -> Product:
    return Product(
        article=article,
        name=product_create.name,
        description=product_create.description,
        author_id = author_id,
        price = product_create.price,
        discount_price = product_create.discount_price,
        stock_quantity = product_create.stock_quantity,
        image = product_create.image,
        minimal_age = product_create.minimal_age,
    )