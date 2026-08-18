from pydantic import BaseModel


class Violation(BaseModel):
    code: str
    name: str
    severity: str
    field: str
    message: str
    recommendation: str


class AuditResult(BaseModel):
    product_id: str
    marketplace: str
    score: int
    violations: list[Violation]
    passed_rules: int
    failed_rules: int