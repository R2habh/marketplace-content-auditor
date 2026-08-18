from app.models.product import Product
from app.models.audit import AuditResult, Violation
from app.rules.registry import GOOGLE_RULES
from app.services.scoring import calculate_score


class Auditor:

    def audit(self, product: Product, marketplace: str) -> AuditResult:
        if marketplace.lower() == "google":
            rules = GOOGLE_RULES
        else:
            raise ValueError(
                f"Unsupported marketplace: {marketplace}"
            )

        violations: list[Violation] = []

        for rule in rules:
            result = rule.check(product)

            if result:
                violations.append(result)

        score = calculate_score(violations)

        return AuditResult(
            product_id=product.id,
            marketplace=marketplace,
            score=score,
            violations=violations,
            passed_rules=len(rules) - len(violations),
            failed_rules=len(violations),
        )