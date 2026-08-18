from app.models.product import Product
from app.services.auditor import Auditor


def test_valid_product():
    product = Product(
        id="1",
        title="Running Shoes",
        description="Comfortable footwear designed for everyday training and workouts. These shoes provide excellent support and durability.",
        brand="TestBrand",
        category="Shoes",
        price=99.99,
        gtin="1234567890123",
        product_url="https://example.com/product",
        image_url="https://example.com/image.jpg",
    )

    result = Auditor().audit(product, "google")

    assert result.failed_rules == 0
    assert result.score == 100


def test_title_too_long():
    product = Product(
        id="1",
        title="A" * 151,
        description="Comfortable footwear designed for everyday training and workouts. These shoes provide excellent support and durability.",
        brand="TestBrand",
        category="Shoes",
        price=99.99,
        gtin="1234567890123",
        product_url="https://example.com/product",
        image_url="https://example.com/image.jpg",
    )

    result = Auditor().audit(product, "google")

    assert result.failed_rules >= 1
    assert any(v.code == "TITLE_TOO_LONG" for v in result.violations)
    assert result.score <= 85  # At least 15 points deducted for ERROR