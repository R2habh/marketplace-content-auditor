import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Marketplace Content Auditor", layout="wide")

st.title("📊 Marketplace Content Auditor Dashboard")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

@st.cache_data
def load_all_results():
    files = list(PROCESSED_DIR.glob("*_audit_*.json"))
    all_data = []
    for f in files:
        marketplace = f.stem.split("_audit_")[0]
        with open(f) as fp:
            data = json.load(fp)
        for d in data:
            d["source_file"] = marketplace
        all_data.extend(data)
    return all_data

all_data = load_all_results()

if not all_data:
    st.warning("No audit results found. Run `python -m scripts.ingest` first.")
    st.stop()

df = pd.DataFrame(all_data)

# Sidebar filters
st.sidebar.header("Filters")
marketplaces = st.sidebar.multiselect(
    "Marketplace", 
    df["source_file"].unique(), 
    default=df["source_file"].unique()
)
score_range = st.sidebar.slider("Score Range", 0, 100, (0, 100))
severity_filter = st.sidebar.multiselect(
    "Violation Severity",
    ["ERROR", "WARNING", "INFO"],
    default=["ERROR", "WARNING"]
)

filtered_df = df[
    (df["source_file"].isin(marketplaces)) &
    (df["score"] >= score_range[0]) &
    (df["score"] <= score_range[1])
]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(filtered_df))
col2.metric("Avg Score", f"{filtered_df['score'].mean():.1f}")
col3.metric("Pass Rate", f"{(filtered_df['passed_rules'] / (filtered_df['passed_rules'] + filtered_df['failed_rules'])).mean()*100:.1f}%")
col4.metric("Files", len(df["source_file"].unique()))

# Score distribution
st.subheader("Score Distribution")
fig = px.histogram(filtered_df, x="score", color="source_file", nbins=20, title="Product Scores by Marketplace")
st.plotly_chart(fig, width='stretch')

# Violation analysis
st.subheader("Top Violations")
violations = []
for _, row in filtered_df.iterrows():
    for v in row["violations"]:
        if v["severity"] in severity_filter:
            violations.append({
                "code": v["code"],
                "severity": v["severity"],
                "field": v["field"],
                "message": v["message"],
                "product": row["title"][:50],
                "marketplace": row["source_file"]
            })

if violations:
    vdf = pd.DataFrame(violations)
    top_codes = vdf["code"].value_counts().head(15)
    fig = px.bar(x=top_codes.values, y=top_codes.index, orientation="h", 
                 title="Top 15 Violation Codes", labels={"x": "Count", "y": "Code"})
    st.plotly_chart(fig, width='stretch')

    # Severity breakdown
    col1, col2 = st.columns(2)
    with col1:
        sev_counts = vdf["severity"].value_counts()
        fig = px.pie(values=sev_counts.values, names=sev_counts.index, title="Violations by Severity")
        st.plotly_chart(fig, width='stretch')
    with col2:
        field_counts = vdf["field"].value_counts().head(10)
        fig = px.bar(x=field_counts.values, y=field_counts.index, orientation="h",
                     title="Top Fields with Violations")
        st.plotly_chart(fig, width='stretch')

# Product table
st.subheader("Products")
display_cols = ["product_id", "title", "brand", "score", "passed_rules", "failed_rules", "source_file"]
st.dataframe(
    filtered_df[display_cols].sort_values("score"),
    width='stretch',
    height=400
)

# Detail view
st.subheader("Product Details")
selected = st.selectbox("Select product", filtered_df["product_id"].unique())
if selected:
    prod = filtered_df[filtered_df["product_id"] == selected].iloc[0]
    st.write(f"**Title:** {prod['title']}")
    st.write(f"**Brand:** {prod['brand']}")
    st.write(f"**Score:** {prod['score']}/100")
    st.write(f"**Passed:** {prod['passed_rules']} | **Failed:** {prod['failed_rules']}")
    
    if prod["violations"]:
        vdf = pd.DataFrame(prod["violations"])
        cols = [c for c in ["code", "severity", "field", "message", "recommendation"] if c in vdf.columns]
        st.dataframe(vdf[cols], width='stretch')
    else:
        st.success("No violations!")