from fastapi import APIRouter
from app.models.product import Product
from app.services.auditor import Auditor


router = APIRouter(prefix="/audit", tags=["Audit"])


auditor = Auditor()


@router.post("/")
async def audit_product(product: Product, marketplace: str = "google"):
    return auditor.audit(product, marketplace)