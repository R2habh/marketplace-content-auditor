import pandas as pd
from pathlib import Path
from app.models.product import Product
from app.services.auditor import Auditor
import json
from datetime import datetime


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

auditor = Auditor()


def parse_price(val) -> float | None:
    if val is None or val == "":
        return None
    try:
        return float(str(val).replace(",", "").replace("$", "").strip())
    except (ValueError, TypeError):
        return None


def map_amazon_row(row) -> Product | None:
    title = str(row.get("title", "")).strip()
    if not title:
        return None

    return Product(
        id=str(row.get("asin", "")),
        title=title,
        description=str(row.get("description", "")).strip(),
        brand=str(row.get("brand", "")).strip() or None,
        category=str(row.get("root_bs_category", "")).strip() or None,
        price=parse_price(row.get("final_price")),
        currency=str(row.get("currency", "USD")).strip() or "USD",
        gtin=str(row.get("gtin", "")).strip() or str(row.get("upc", "")).strip() or None,
        product_url=str(row.get("url", "")).strip() or None,
        image_url=str(row.get("image_url", "")).strip() or None,
    )


def map_shopee_row(row) -> Product | None:
    title = str(row.get("title", "")).strip()
    if not title:
        return None

    return Product(
        id=str(row.get("id", "")),
        title=title,
        description=str(row.get("Product Description", "")).strip(),
        brand=str(row.get("brand", "")).strip() or None,
        category=str(row.get("breadcrumb", "")).strip() or None,
        price=parse_price(row.get("final_price")),
        currency=str(row.get("currency", "USD")).strip() or "USD",
        gtin=None,
        product_url=str(row.get("url", "")).strip() or None,
        image_url=str(row.get("image", "")).strip() or None,
    )


def map_walmart_row(row) -> Product | None:
    title = str(row.get("product_name", "")).strip()
    if not title:
        return None

    return Product(
        id=str(row.get("product_id", "")),
        title=title,
        description=str(row.get("description", "")).strip(),
        brand=str(row.get("brand", "")).strip() or None,
        category=str(row.get("category_name", "")).strip() or None,
        price=parse_price(row.get("final_price")),
        currency=str(row.get("currency", "USD")).strip() or "USD",
        gtin=str(row.get("gtin", "")).strip() or str(row.get("upc", "")).strip() or None,
        product_url=str(row.get("url", "")).strip() or None,
        image_url=str(row.get("main_image", "")).strip() or None,
    )


MAPPERS = {
    "amazon-products.csv": map_amazon_row,
    "shopee-products.csv": map_shopee_row,
    "walmart-products.csv": map_walmart_row,
}


def process_file(csv_file: Path, limit: int | None = None):
    print(f"Processing {csv_file.name}...")
    mapper = MAPPERS.get(csv_file.name)
    if not mapper:
        print(f"  No mapper for {csv_file.name}")
        return

    df = pd.read_csv(csv_file, dtype=str, low_memory=False)
    if limit:
        df = df.head(limit)

    results = []
    for idx, row in df.iterrows():
        product = mapper(row)
        if not product:
            continue

        result = auditor.audit(product, "google")
        results.append({
            "product_id": product.id,
            "title": product.title[:80],
            "brand": product.brand,
            "score": result.score,
            "passed_rules": result.passed_rules,
            "failed_rules": result.failed_rules,
            "violations": [
                {"code": v.code, "severity": v.severity, "field": v.field, "message": v.message}
                for v in result.violations
            ],
        })

        if idx % 100 == 0 and idx > 0:
            print(f"  Processed {idx} products...")

    output_file = OUTPUT_DIR / f"{csv_file.stem}_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Completed: {len(results)} products audited")
    print(f"  Results saved to {output_file}")

    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
        print(f"  Average score: {avg_score:.1f}")


if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    for csv_file in RAW_DIR.glob("*.csv"):
        process_file(csv_file, limit)