from app.models.product import Product
from app.models.audit import Violation
from app.rules.base import Rule
from app.services.text_utils import (
    contains_promotional_text,
    uppercase_ratio,
    repeated_words,
    normalize_text,
)


class TitleEmptyRule(Rule):
    code = "TITLE_EMPTY"
    name = "Title is empty"
    severity = "ERROR"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        if not product.title or not product.title.strip():
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="Product title is empty.",
                recommendation="Add a clear product title.",
            )

        return None


class TitleTooLongRule(Rule):
    code = "TITLE_TOO_LONG"
    name = "Title exceeds maximum length"
    severity = "ERROR"
    field = "title"

    MAX_LENGTH = 150

    def check(self, product: Product) -> Violation | None:
        length = len(product.title)

        if length > self.MAX_LENGTH:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Title contains {length} characters.",
                recommendation=(
                    f"Reduce the title to {self.MAX_LENGTH} "
                    "characters or fewer."
                ),
            )

        return None


class TitlePromotionalTextRule(Rule):
    code = "TITLE_PROMOTIONAL_TEXT"
    name = "Title contains promotional text"
    severity = "WARNING"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        phrase = contains_promotional_text(product.title)

        if phrase:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Promotional phrase detected: '{phrase}'.",
                recommendation=(
                    "Remove promotional language from the product title."
                ),
            )

        return None


class TitleExcessiveCapsRule(Rule):
    code = "TITLE_EXCESSIVE_CAPS"
    name = "Title uses excessive capitalization"
    severity = "WARNING"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        if uppercase_ratio(product.title) > 0.70:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="More than 70% of alphabetic characters are uppercase.",
                recommendation="Use normal title capitalization.",
            )

        return None


class TitleExcessivePunctuationRule(Rule):
    code = "TITLE_EXCESSIVE_PUNCTUATION"
    name = "Title contains excessive punctuation"
    severity = "WARNING"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        punctuation_count = sum(1 for c in product.title if c in "!@#$%^&*()_+-=[]{}|;':\",./<>?")
        total_chars = len(product.title)

        if total_chars > 0 and (punctuation_count / total_chars) > 0.15:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Title contains {punctuation_count} punctuation characters ({punctuation_count/total_chars*100:.1f}%).",
                recommendation="Reduce punctuation in the product title.",
            )

        return None


class TitleRepeatedWordsRule(Rule):
    code = "TITLE_REPEATED_WORDS"
    name = "Title contains repeated words"
    severity = "WARNING"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        repeats = repeated_words(product.title)

        if repeats:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Repeated words detected: {', '.join(repeats)}.",
                recommendation="Avoid repeating words in the product title.",
            )

        return None


class TitleInvalidSymbolsRule(Rule):
    code = "TITLE_INVALID_SYMBOLS"
    name = "Title contains invalid symbols"
    severity = "ERROR"
    field = "title"

    INVALID_SYMBOLS = set("~`^|\\{}[]")

    def check(self, product: Product) -> Violation | None:
        found = [c for c in product.title if c in self.INVALID_SYMBOLS]

        if found:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message=f"Invalid symbols detected: {', '.join(set(found))}.",
                recommendation="Remove invalid symbols from the product title.",
            )

        return None