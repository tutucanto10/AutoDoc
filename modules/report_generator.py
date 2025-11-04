from reportlab.lib.pagesizes import A4
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import black, lightgrey
from pathlib import Path
import pandas as pd

def _img(path, width=500):
    try:
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))
    except Exception:
        return None

def generate_pdf(title, metrics, chart_paths, output_dir, logo_path=None, ai_summary=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / "report.pdf"

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Header
    if logo_path and Path(logo_path).exists():
        logo = _img(logo_path, width=140)
        if logo:
            story.append(logo)
            story.append(Spacer(1, 12))

    h = styles["Title"]
    h.alignment = TA_CENTER
    story.append(Paragraph(title, h))
    story.append(Spacer(1, 12))

    # KPIs table
    kpi_data = [
        ["Total Rows", metrics.get("total_rows", "-")],
        ["Numeric Columns", ", ".join(metrics.get("numeric_columns", [])) or "-"]
    ]
    # Append sums
    if metrics.get("sum_by_numeric"):
        for k, v in metrics["sum_by_numeric"].items():
            kpi_data.append([f"Sum({k})", f"{v:.2f}"])

    table = Table(kpi_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1, black),
        ("INNERGRID", (0,0), (-1,-1), 0.5, black),
        ("BACKGROUND", (0,0), (-1,0), lightgrey),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # AI Summary
    if ai_summary:
        story.append(Paragraph("<b>AI Summary</b>", styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(ai_summary.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 12))

    # Charts
    for p in chart_paths:
        img = _img(p, width=400)
        if img:
            story.append(img)
            story.append(Spacer(1, 12))

    doc.build(story)
    return str(pdf_path)

def generate_excel_report(df: pd.DataFrame, metrics: dict, out_path):
    out_path = Path(out_path)
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        kpi_df = pd.DataFrame(
            [("total_rows", metrics.get("total_rows", 0))] +
            [("numeric_columns", ", ".join(metrics.get("numeric_columns", [])))] +
            [(f"sum_{k}", v) for k, v in metrics.get("sum_by_numeric", {}).items()]
        )
        kpi_df.to_excel(writer, index=False, header=["metric", "value"], sheet_name="KPIs")
    return str(out_path)
