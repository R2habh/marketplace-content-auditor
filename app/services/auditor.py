from app.models.product import Product
from app.rules.registry import GOOGLE_RULES


class Auditor:

    def audit(self, product: Product, marketplace: str):
        if marketplace.lower() == "google":
            rules = GOOGLE_RULES
        else:
            raise ValueError(
                f"Unsupported marketplace: {marketplace}"
            )

        violations = []

        for rule in rules:
            result = rule.check(product)

            if result:
                violations.append(result)

        return {
            "product_id": product.id,
            "marketplace": marketplace,
            "violations": violations,
            "violation_count": len(violations),
        }