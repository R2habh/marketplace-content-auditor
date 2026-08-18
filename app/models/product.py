from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str
    title: str = ""
    description: str = ""
    brand: str | None = None
    category: str | None = None
    sku: str | None = None
    gtin: str | None = None
    price: float | None = None
    currency: str | None = None
    product_url: str | None = None
    image_url: str | None = None
