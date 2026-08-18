# Marketplace Content Auditor

A production-ready content auditing system for ecommerce product data. Validates products against configurable marketplace rules (Google Shopping, Amazon, etc.) with scoring, violation detection, and a Streamlit dashboard.

## Features

- **Rule Engine**: 22+ validation rules for Google Shopping (titles, descriptions, fields, content quality)
- **Scoring System**: Weighted severity scoring (ERROR=-15, WARNING=-5, INFO=-1) with 0-100 scale
- **Multi-Marketplace Data Ingestion**: Processes Amazon, Shopee, Walmart CSVs
- **REST API**: FastAPI with automatic OpenAPI docs
- **Dashboard**: Streamlit visualization with filters, charts, and drill-down
- **Tests**: Pytest suite with 100% pass rate

## Architecture

```
├── app/
│   ├── api/audit.py           # POST /audit/ endpoint
│   ├── models/
│   │   ├── product.py         # Product Pydantic model
│   │   └── audit.py           # Violation & AuditResult models
│   ├── rules/
│   │   ├── base.py            # Abstract Rule class
│   │   ├── registry.py        # GOOGLE_RULES registry
│   │   └── marketplaces/google/
│   │       ├── title.py       # 7 title rules
│   │       ├── description.py # 6 description rules
│   │       ├── fields.py      # 6 missing field rules
│   │       └── content.py     # 3 content quality rules
│   ├── services/
│   │   ├── auditor.py         # Core audit orchestration
│   │   ├── scoring.py         # Score calculation
│   │   └── text_utils.py      # Shared text processing
│   └── main.py                # FastAPI app
├── scripts/
│   └── ingest.py              # CSV → Product → Audit pipeline
├── data/
│   ├── raw/                   # Source CSVs (gitignored)
│   ├── sample/                # Sample data
│   └── processed/             # Audit results JSON (gitignored)
├── tests/
│   └── test_auditor.py        # Unit tests
├── dashboard.py               # Streamlit dashboard
└── requirements.txt
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Raw Data (Optional)
Place CSV files in `data/raw/`:
- `amazon-products.csv`
- `shopee-products.csv` 
- `walmart-products.csv`

### 3. Run Data Ingestion
```bash
# Test with 10 products per file
python -m scripts.ingest 10

# Full processing
python -m scripts.ingest
```

### 4. Start API Server
```bash
python -m uvicorn app.main:app --reload
```
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### 5. Launch Dashboard
```bash
streamlit run dashboard.py
```
- Dashboard: http://localhost:8501

## API Usage

### Audit a Product
```bash
curl -X POST http://127.0.0.1:8000/audit/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "1",
    "title": "Running Shoes",
    "description": "Comfortable shoes for everyday training.",
    "brand": "Nike",
    "category": "Shoes",
    "price": 99.99,
    "gtin": "1234567890123",
    "product_url": "https://example.com/product",
    "image_url": "https://example.com/img.jpg"
  }'
```

### Response
```json
{
  "product_id": "1",
  "marketplace": "google",
  "score": 100,
  "passed_rules": 22,
  "failed_rules": 0,
  "violations": []
}
```

## Rules Implemented (Google Shopping)

| Category | Rules |
|----------|-------|
| **Title** | Empty, Too Long (>150), Promotional Text, Excessive Caps (>70%), Excessive Punctuation (>15%), Repeated Words, Invalid Symbols |
| **Description** | Empty, Too Long (>5000), Too Short (<50), Promotional Text, Excessive Caps (>30%), Repeated Content |
| **Required Fields** | Brand, Category, GTIN, Price, Product URL, Image URL |
| **Content Quality** | Keyword Stuffing, Duplicate Title/Description, Suspicious Marketing Claims |

## Scoring

| Severity | Deduction |
|----------|-----------|
| ERROR    | -15       |
| WARNING  | -5        |
| INFO     | -1        |

Score = max(0, 100 - sum(deductions))

## Dashboard Features

- **KPIs**: Total products, average score, pass rate
- **Score Distribution**: Histogram by marketplace
- **Top Violations**: Bar chart of most common issues
- **Severity Breakdown**: Pie chart
- **Field Analysis**: Which fields have most violations
- **Product Table**: Sortable, filterable list
- **Drill-down**: Click product for violation details with recommendations

## Dashboard Preview

![Dashboard Overview](docs/dashboard.png)

*Run `streamlit run dashboard.py` and open http://localhost:8501*

## Running Tests

```bash
python -m pytest
```

## Project Structure

```
marketplace-content-auditor/
├── app/                 # Core application
├── scripts/             # Data processing scripts
├── data/                # Data directories
├── tests/               # Unit tests
├── dashboard.py         # Streamlit dashboard
├── requirements.txt     # Dependencies
├── .gitignore
└── README.md
```

## Extending Rules

1. Create new rule in `app/rules/marketplaces/google/`
2. Inherit from `Rule` base class
3. Register in `app/rules/registry.py`

```python
class MyCustomRule(Rule):
    code = "MY_CUSTOM_RULE"
    name = "Custom Rule Name"
    severity = "WARNING"
    field = "title"

    def check(self, product: Product) -> Violation | None:
        if some_condition:
            return Violation(
                code=self.code,
                name=self.name,
                severity=self.severity,
                field=self.field,
                message="...",
                recommendation="..."
            )
        return None
```

## License

MIT