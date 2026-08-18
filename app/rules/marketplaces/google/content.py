from app.models.product import Product
from app.models.audit import Violation
from app.rules.base import Rule
from app.services.text_utils import (
    normalize_text,
    repeated_words,
)


class KeywordStuffingRule(Rule):
    code = "KEYWORD_STUFFING"
    name = "Keyword stuffing detected"
    severity = "WARNING"
    field = "title,description"

    def check(self, product: Product) -> Violation | None:
        if not product.title or not product.description:
            return None

        title_words = set(normalize_text(product.title).lower().split())
        desc_words = set(normalize_text(product.description).lower().split())

        common = title_words & desc_words

        if len(common) > 10:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Title and description share {len(common)} common words.",
                recommendation=(
                    "Ensure title and description are complementary, not repetitive."
                ),
            )

        return None


class DuplicateTitleDescriptionRule(Rule):
    code = "DUPLICATE_TITLE_DESCRIPTION"
    name = "Title and description are too similar"
    severity = "WARNING"
    field = "title,description"

    def check(self, product: Product) -> Violation | None:
        if not product.title or not product.description:
            return None

        title_norm = normalize_text(product.title).lower()
        desc_norm = normalize_text(product.description).lower()

        if title_norm == desc_norm:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Title and description are identical.",
                recommendation="Make the description unique from the title.",
            )

        if title_norm in desc_norm or desc_norm in title_norm:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Title is a substring of description or vice versa.",
                recommendation="Ensure title and description are distinct.",
            )

        return None


class SuspiciousMarketingClaimRule(Rule):
    code = "SUSPICIOUS_MARKETING_CLAIM"
    name = "Suspicious marketing claim detected"
    severity = "WARNING"
    field = "title,description"

    SUSPICIOUS_PATTERNS = [
        "guaranteed",
        "miracle",
        "instant",
        "overnight",
        "secret",
        "proven",
        "scientifically proven",
        "doctor recommended",
        "fda approved",
        "100% effective",
        "risk free",
        "no side effects",
    ]

    def check(self, product: Product) -> Violation | None:
        text = f"{product.title or ''} {product.description or ''}".lower()

        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in text:
                return Violation(
                    code=self.code,
                    name=self.name,
                    severity=self.severity,
                    field=self.field,
                    message=f"Suspicious claim detected: '{pattern}'.",
                    recommendation=(
                        "Remove unverifiable marketing claims from product content."
                    ),
                )

        return None