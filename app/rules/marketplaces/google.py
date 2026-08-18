from app.models.product import Product
from app.rules.base import Rule


class TitleTooLongRule(Rule):
    code = "TITLE_TOO_LONG"
    name = "Title exceeds maximum length"
    severity = "ERROR"

    MAX_LENGTH = 150

    def check(self, product: Product):
        if len(product.title) > self.MAX_LENGTH:
            return {
                "code": self.code,
                "severity": self.severity,
                "message": (
                    f"Title contains {len(product.title)} characters; "
                    f"maximum is {self.MAX_LENGTH}."
                ),
            }

        return None