# AutoDoc
Gerador inteligente de relatórios corporativos em **Python + IA**.

## ✅ Recursos
- Importa **CSV/XLSX/JSON**
- KPIs automáticos e **gráficos** (Matplotlib)
- Exporta **PDF** (ReportLab) e **Excel** (XLSXWriter)
- **Resumo por IA** com LangChain + OpenAI (opcional)
- Interface **Streamlit** + CLI

## 🧪 Exemplo rápido (dados de vendas)
Um dataset de exemplo está em `data/sample_sales.csv`.

## 🚀 Como rodar
```bash
# 1) Crie o ambiente
python -m venv .venv && . .venv/bin/activate  # (Linux/Mac)
# Windows: python -m venv .venv && .\.venv\Scripts\activate

# 2) Instale dependências
pip install -r requirements.txt

# 3) (Opcional) Configure a IA
export OPENAI_API_KEY="sk-..."  # Windows: set OPENAI_API_KEY=...

# 4) CLI: gerar relatório
python main.py -i data/sample_sales.csv -o output --title "Relatório de Vendas" --excel --ai

# 5) Interface web (Streamlit)
streamlit run interface/app.py
```

## 🧱 Estrutura
```
AutoDoc/
├── main.py
├── data/
├── modules/
│   ├── reader.py
│   ├── analyzer.py
│   ├── report_generator.py
│   └── ai_summary.py
├── interface/
│   └── app.py
├── assets/
├── requirements.txt
└── README.md
```

## 📝 Notas
- O resumo por IA cai para um **fallback** automático se não houver `OPENAI_API_KEY`.
- Os gráficos são salvos no diretório de saída temporário e inseridos no PDF.
- O Excel contém abas `Data` e `KPIs`.
