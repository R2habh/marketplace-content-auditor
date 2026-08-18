from fastapi import FastAPI

from app.api.audit import router as audit_router


app = FastAPI(
    title="Marketplace Content Auditor",
    description="Audits ecommerce product content against configurable marketplace rules.",
    version="0.1.0",
)


app.include_router(audit_router)


@app.get("/")
async def root():
    return {
        "name": "Marketplace Content Auditor",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}