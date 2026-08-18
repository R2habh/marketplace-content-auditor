from app.rules.marketplaces.google.title import (
    TitleEmptyRule,
    TitleTooLongRule,
    TitlePromotionalTextRule,
    TitleExcessiveCapsRule,
    TitleExcessivePunctuationRule,
    TitleRepeatedWordsRule,
    TitleInvalidSymbolsRule,
)
from app.rules.marketplaces.google.description import (
    DescriptionEmptyRule,
    DescriptionTooLongRule,
    DescriptionTooShortRule,
    DescriptionPromotionalTextRule,
    DescriptionExcessiveCapsRule,
    DescriptionRepeatedContentRule,
)
from app.rules.marketplaces.google.fields import (
    MissingBrandRule,
    MissingCategoryRule,
    MissingGTINRule,
    MissingPriceRule,
    MissingProductURLRule,
    MissingImageURLRule,
)
from app.rules.marketplaces.google.content import (
    KeywordStuffingRule,
    DuplicateTitleDescriptionRule,
    SuspiciousMarketingClaimRule,
)


GOOGLE_RULES = [
    TitleEmptyRule(),
    TitleTooLongRule(),
    TitlePromotionalTextRule(),
    TitleExcessiveCapsRule(),
    TitleExcessivePunctuationRule(),
    TitleRepeatedWordsRule(),
    TitleInvalidSymbolsRule(),

    DescriptionEmptyRule(),
    DescriptionTooLongRule(),
    DescriptionTooShortRule(),
    DescriptionPromotionalTextRule(),
    DescriptionExcessiveCapsRule(),
    DescriptionRepeatedContentRule(),

    MissingBrandRule(),
    MissingCategoryRule(),
    MissingGTINRule(),
    MissingPriceRule(),
    MissingProductURLRule(),
    MissingImageURLRule(),

    KeywordStuffingRule(),
    DuplicateTitleDescriptionRule(),
    SuspiciousMarketingClaimRule(),
]