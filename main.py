#!/usr/bin/env python3
"""
AutoDoc - CLI entrypoint
"""
from modules.reader import read_data
from modules.analyzer import analyze_data
from modules.report_generator import generate_pdf, generate_excel_report
from modules.ai_summary import generate_ai_summary
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="AutoDoc - Intelligent report generator")
    parser.add_argument("--input", "-i", required=True, help="Path to data file (csv/xlsx/json)")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    parser.add_argument("--title", "-t", default="AutoDoc Report", help="Report title")
    parser.add_argument("--logo", "-l", default=None, help="Path to logo image (optional)")
    parser.add_argument("--excel", action="store_true", help="Also generate Excel report")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--ai", action="store_true", help="Generate AI summary (requires OPENAI_API_KEY)")

    args = parser.parse_args()
    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)

    df = read_data(args.input)
    metrics, charts = analyze_data(df, output_dir=outdir)

    ai_text = None
    if args.ai:
        prompt_context = {
            "title": args.title,
            "metrics": metrics,
            "columns": list(df.columns),
            "row_count": len(df)
        }
        ai_text = generate_ai_summary(prompt_context)

    if not args.no_pdf:
        pdf_path = generate_pdf(
            title=args.title,
            metrics=metrics,
            chart_paths=charts,
            output_dir=outdir,
            logo_path=args.logo,
            ai_summary=ai_text
        )
        print(f"[AutoDoc] PDF generated at: {pdf_path}")

    if args.excel:
        xlsx_path = generate_excel_report(df, metrics, outdir / "report.xlsx")
        print(f"[AutoDoc] Excel generated at: {xlsx_path}")

if __name__ == "__main__":
    main()
