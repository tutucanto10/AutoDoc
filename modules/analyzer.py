import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def _safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")

def analyze_data(df: pd.DataFrame, output_dir: Path):
    """
    Produces basic KPIs and charts. Saves charts to disk and returns their paths.
    KPIs:
      - total_rows
      - numeric_columns
      - sum_by_numeric
      - top_categories (if a 'category' or 'produto' column exists)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics = {
        "total_rows": len(df),
        "columns": list(df.columns),
        "numeric_columns": [],
        "sum_by_numeric": {},
        "top_categories": {}
    }

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    metrics["numeric_columns"] = numeric_cols

    # Summaries for numeric columns
    for c in numeric_cols:
        metrics["sum_by_numeric"][c] = float(_safe_numeric(df[c]).sum(skipna=True))

    # Try to infer a category column
    cat_col = None
    for guess in ["category", "Category", "produto", "Produto", "product", "Product"]:
        if guess in df.columns:
            cat_col = guess
            break

    charts = []

    # Chart 1: row count bar
    fig1 = plt.figure()
    plt.bar(["rows"], [len(df)])
    plt.title("Total Rows")
    path1 = output_dir / "chart_total_rows.png"
    fig1.savefig(path1, bbox_inches="tight")
    plt.close(fig1)
    charts.append(str(path1))

    # Chart 2: sums of numeric columns (if any)
    if numeric_cols:
        sums = [metrics["sum_by_numeric"][c] for c in numeric_cols]
        fig2 = plt.figure()
        plt.bar(numeric_cols, sums)
        plt.title("Sum by Numeric Column")
        plt.xticks(rotation=30, ha="right")
        path2 = output_dir / "chart_sum_numeric.png"
        fig2.savefig(path2, bbox_inches="tight")
        plt.close(fig2)
        charts.append(str(path2))

    # Chart 3: top categories if category-like column exists
    if cat_col:
        counts = df[cat_col].astype(str).value_counts().head(10)
        metrics["top_categories"] = counts.to_dict()
        fig3 = plt.figure()
        plt.bar(counts.index.tolist(), counts.values.tolist())
        plt.title(f"Top {cat_col} (count)")
        plt.xticks(rotation=30, ha="right")
        path3 = output_dir / "chart_top_categories.png"
        fig3.savefig(path3, bbox_inches="tight")
        plt.close(fig3)
        charts.append(str(path3))

    return metrics, charts
