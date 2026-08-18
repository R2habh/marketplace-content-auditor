from app.models.product import Product
from app.models.audit import Violation
from app.rules.base import Rule


class MissingBrandRule(Rule):
    code = "MISSING_BRAND"
    name = "Brand is missing"
    severity = "ERROR"
    field = "brand"

    def check(self, product: Product) -> Violation | None:
        if not product.brand or not product.brand.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product brand is missing.",
                recommendation="Add the product's brand name.",
            )

        return None


class MissingCategoryRule(Rule):
    code = "MISSING_CATEGORY"
    name = "Category is missing"
    severity = "ERROR"
    field = "category"

    def check(self, product: Product) -> Violation | None:
        if not product.category or not product.category.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product category is missing.",
                recommendation="Add a Google product category.",
            )

        return None


class MissingGTINRule(Rule):
    code = "MISSING_GTIN"
    name = "GTIN is missing"
    severity = "WARNING"
    field = "gtin"

    def check(self, product: Product) -> Violation | None:
        if not product.gtin or not product.gtin.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product GTIN (Global Trade Item Number) is missing.",
                recommendation="Add a valid GTIN, UPC, EAN, or ISBN.",
            )

        return None


class MissingPriceRule(Rule):
    code = "MISSING_PRICE"
    name = "Price is missing"
    severity = "ERROR"
    field = "price"

    def check(self, product: Product) -> Violation | None:
        if product.price is None:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product price is missing.",
                recommendation="Add the product price.",
            )

        return None


class MissingProductURLRule(Rule):
    code = "MISSING_PRODUCT_URL"
    name = "Product URL is missing"
    severity = "ERROR"
    field = "product_url"

    def check(self, product: Product) -> Violation | None:
        if not product.product_url or not product.product_url.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product landing page URL is missing.",
                recommendation="Add the product's landing page URL.",
            )

        return None


class MissingImageURLRule(Rule):
    code = "MISSING_IMAGE_URL"
    name = "Image URL is missing"
    severity = "ERROR"
    field = "image_url"

    def check(self, product: Product) -> Violation | None:
        if not product.image_url or not product.image_url.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product image URL is missing.",
                recommendation="Add at least one product image URL.",
            )

        return None