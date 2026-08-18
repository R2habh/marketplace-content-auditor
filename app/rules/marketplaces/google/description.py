from app.models.product import Product
from app.models.audit import Violation
from app.rules.base import Rule
from app.services.text_utils import (
    contains_promotional_text,
    uppercase_ratio,
    repeated_words,
    normalize_text,
)


class DescriptionEmptyRule(Rule):
    code = "DESCRIPTION_EMPTY"
    name = "Description is empty"
    severity = "ERROR"
    field = "description"

    def check(self, product: Product) -> Violation | None:
        if not product.description or not product.description.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product description is empty.",
                recommendation="Add a product description.",
            )

        return None


class DescriptionTooLongRule(Rule):
    code = "DESCRIPTION_TOO_LONG"
    name = "Description exceeds maximum length"
    severity = "WARNING"
    field = "description"

    MAX_LENGTH = 5000

    def check(self, product: Product) -> Violation | None:
        if not product.description:
            return None

        length = len(product.description)

        if length > self.MAX_LENGTH:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Description contains {length} characters.",
                recommendation=(
                    f"Reduce the description to {self.MAX_LENGTH} "
                    "characters or fewer."
                ),
            )

        return None


class DescriptionTooShortRule(Rule):
    code = "DESCRIPTION_TOO_SHORT"
    name = "Description is too short"
    severity = "WARNING"
    field = "description"

    MIN_LENGTH = 50

    def check(self, product: Product) -> Violation | None:
        if not product.description:
            return None

        length = len(product.description)

        if length < self.MIN_LENGTH:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Description contains only {length} characters.",
                recommendation=(
                    f"Expand the description to at least {self.MIN_LENGTH} "
                    "characters."
                ),
            )

        return None


class DescriptionPromotionalTextRule(Rule):
    code = "DESCRIPTION_PROMOTIONAL_TEXT"
    name = "Description contains promotional text"
    severity = "WARNING"
    field = "description"

    def check(self, product: Product) -> Violation | None:
        if not product.description:
            return None

        phrase = contains_promotional_text(product.description)

        if phrase:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Promotional phrase detected: '{phrase}'.",
                recommendation=(
                    "Remove promotional language from the product description."
                ),
            )

        return None


class DescriptionExcessiveCapsRule(Rule):
    code = "DESCRIPTION_EXCESSIVE_CAPS"
    name = "Description uses excessive capitalization"
    severity = "WARNING"
    field = "description"

    def check(self, product: Product) -> Violation | None:
        if not product.description:
            return None

        if uppercase_ratio(product.description) > 0.30:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="More than 30% of alphabetic characters are uppercase.",
                recommendation="Use normal sentence capitalization.",
            )

        return None


class DescriptionRepeatedContentRule(Rule):
    code = "DESCRIPTION_REPEATED_CONTENT"
    name = "Description contains repeated content"
    severity = "WARNING"
    field = "description"

    def check(self, product: Product) -> Violation | None:
        if not product.description:
            return None

        repeats = repeated_words(product.description)

        if repeats:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Repeated words detected: {', '.join(repeats)}.",
                recommendation="Avoid repeating words excessively in the description.",
            )

        return None