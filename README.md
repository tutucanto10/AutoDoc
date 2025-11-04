📄 ### AutoDoc – Intelligent Report Generator with AI

AutoDoc is a smart, automated report generator built with Python + AI, designed to transform raw data (Excel, CSV, or JSON) into insightful PDF and Excel reports — complete with KPIs, charts, and AI-generated summaries.

------

🚀 ### Features

📊 Automatic data analysis from CSV, Excel, or JSON
📈 Charts and KPIs generated via Matplotlib + Pandas
🧠 AI summaries using LangChain + OpenAI (optional)
🧾 Export to PDF (ReportLab) and Excel (XLSXWriter)
💻 Modern web interface built with Streamlit
🧰 Command-line tool (CLI) included for power users
💬 Fallback summary if no API key is provided

------

🧠 ### Tech Stack

Category	Technologies
Language	Python 3.11+
Frontend	Streamlit
Backend / Data	Pandas, Matplotlib
Report Generation	ReportLab, XlsxWriter
AI / NLP	LangChain, OpenAI API
Storage	SQLite (optional)

------

🗂️ ### Project Structure

AutoDoc/
├── main.py
├── data/
│   └── sample_sales.csv
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

------

⚙️ ### Installation
# 1️⃣ Create a virtual environment
python -m venv .venv
# Activate it:
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2️⃣ Install dependencies
pip install -r requirements.txt

------

🤖 ### Optional: Enable AI Summaries

To allow AI-generated insights, set your OpenAI API key:

# Windows (cmd)
set OPENAI_API_KEY=sk-...
# macOS/Linux (bash/zsh)
export OPENAI_API_KEY="sk-..."

------

🧮 ### CLI Usage
python main.py -i data/sample_sales.csv -o output --title "Sales Report" --excel --ai


Arguments:

Flag	Description
-i / --input	Path to input file (CSV/XLSX/JSON)
-o / --output	Output folder
-t / --title	Report title
--excel	Generate Excel report
--ai	Include AI summary (requires API key)
--no-pdf	Skip PDF generation

------

🌐 ### Streamlit Web Interface

Start the interactive app with:

streamlit run interface/app.py

Then open your browser (default: http://localhost:8501) to:

Upload files
Preview data and KPIs
Generate PDF and Excel reports
Optionally use AI to summarize insights

------

🧩 ### Example Dataset

A sample sales dataset is provided at:

data/sample_sales.csv

------

🪶 ### Example Output

PDF Report: Includes logo, title, KPIs table, charts, and AI insights

Excel Report: Two sheets (Data and KPIs)

Charts: Automatically saved and embedded in the PDF

------

💡 ### Future Improvements (Next Milestones)

Add time-series and regional KPIs
Include custom color themes and PDF templates
Enable direct SharePoint / Supabase upload
Add user authentication (for web version)

------

👨‍💻 Author

Artur Canto
Python Developer • Automation & AI Enthusiast
📍 Rio de Janeiro, Brazil
