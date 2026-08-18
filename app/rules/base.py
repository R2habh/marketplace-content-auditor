from abc import ABC, abstractmethod
from app.models.product import Product


class Rule(ABC):
    code: str
    name: str
    severity: str

    @abstractmethod
    def check(self, product: Product) -> dict | None:
        pass