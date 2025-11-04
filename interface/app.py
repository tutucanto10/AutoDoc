import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pathlib import Path
from modules.reader import read_data
from modules.analyzer import analyze_data
from modules.report_generator import generate_pdf, generate_excel_report
from modules.ai_summary import generate_ai_summary
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="AutoDoc", page_icon="📄", layout="wide")

st.title("📄 AutoDoc — Gerador de Relatórios com IA")
st.write("Carregue um arquivo (CSV/XLSX/JSON), veja KPIs e gere um PDF/Excel com resumo por IA.")

uploaded = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx", "json"])
logo = st.file_uploader("Logo (opcional)", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Título do relatório", "Relatório de Vendas")
with col2:
    use_ai = st.checkbox("Gerar resumo com IA (OPENAI_API_KEY)", value=False)

if uploaded is not None:
    # Persist uploaded file to a temp path so pandas can read it
    tmpdir = tempfile.TemporaryDirectory()
    data_path = Path(tmpdir.name) / uploaded.name
    with open(data_path, "wb") as f:
        f.write(uploaded.getbuffer())

    df = read_data(data_path)
    st.subheader("Prévia dos dados")
    st.dataframe(df.head(50))

    metrics, charts = analyze_data(df, output_dir=Path(tmpdir.name))
    st.subheader("KPIs & Gráficos")
    st.json(metrics)

    for p in charts:
        st.image(str(p), use_column_width=True)

    ai_text = None
    if use_ai:
        ctx = {"title": title, "metrics": metrics, "columns": list(df.columns), "row_count": len(df)}
        ai_text = generate_ai_summary(ctx)
        st.subheader("Resumo por IA")
        st.write(ai_text)

    gen_col1, gen_col2 = st.columns(2)
    with gen_col1:
        if st.button("Gerar PDF"):
            logo_path = None
            if logo is not None:
                logo_path = Path(tmpdir.name) / logo.name
                with open(logo_path, "wb") as f:
                    f.write(logo.getbuffer())
            pdf_path = generate_pdf(title, metrics, charts, Path(tmpdir.name), logo_path=logo_path, ai_summary=ai_text)
            with open(pdf_path, "rb") as f:
                st.download_button("Baixar PDF", data=f, file_name="report.pdf", mime="application/pdf")
    with gen_col2:
        if st.button("Gerar Excel"):
            xlsx_path = generate_excel_report(df, metrics, Path(tmpdir.name) / "report.xlsx")
            with open(xlsx_path, "rb") as f:
                st.download_button("Baixar Excel", data=f, file_name="report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Envie um arquivo para começar.")
