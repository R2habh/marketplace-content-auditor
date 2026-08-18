from app.models.product import Product
from app.services.auditor import Auditor


def test_valid_title():
    product = Product(
        id="1",
        title="Running Shoes",
        description="Running shoes for everyday training.",
    )

    result = Auditor().audit(product, "google")

    assert result["violation_count"] == 0


def test_title_too_long():
    product = Product(
        id="1",
        title="A" * 151,
        description="Test",
    )

    result = Auditor().audit(product, "google")

    assert result["violation_count"] == 1
    assert result["violations"][0]["code"] == "TITLE_TOO_LONG"