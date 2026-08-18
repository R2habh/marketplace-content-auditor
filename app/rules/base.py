from abc import ABC, abstractmethod
from app.models.product import Product
from app.models.audit import Violation


class Rule(ABC):
    code: str
    name: str
    severity: str
    field: str

    @abstractmethod
    def check(self, product: Product) -> Violation | None:
        raise NotImplementedError