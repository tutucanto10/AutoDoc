import os
from typing import Optional

def _format_context(ctx: dict) -> str:
    parts = [
        f"Title: {ctx.get('title')}",
        f"Rows: {ctx.get('row_count')}",
        f"Columns: {', '.join(ctx.get('columns', []))}",
        "Numeric summaries: " + ", ".join([f"{k}: {v}" for k, v in ctx.get('metrics', {}).get('sum_by_numeric', {}).items()])
    ]
    return "\n".join(parts)

def generate_ai_summary(context: dict) -> Optional[str]:
    """
    Uses OpenAI via LangChain if OPENAI_API_KEY is available.
    Falls back to a simple rule-based summary otherwise.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        if api_key:
            # Lazy import to keep base install light
            from langchain_openai import ChatOpenAI
            from langchain.prompts import ChatPromptTemplate

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            prompt = ChatPromptTemplate.from_template(
                "You are a data analyst. Given the context below, write a concise, executive summary (5-8 bullet points) in Portuguese with insights, risks, and next steps.\n\nContexto:\n{context}"
            )
            chain = prompt | llm
            result = chain.invoke({"context": _format_context(context)})
            text = result.content if hasattr(result, "content") else str(result)
            return text.strip()
        else:
            ctx = context
            nums = ctx.get("metrics", {}).get("sum_by_numeric", {})
            highlights = ", ".join([f"{k} soma={v:.2f}" for k, v in nums.items()]) or "Sem colunas numéricas."
            return (
                "Resumo automático (fallback):\n"
                f"- Linhas processadas: {ctx.get('row_count')}\n"
                f"- Colunas: {', '.join(ctx.get('columns', []))}\n"
                f"- Destaques: {highlights}\n"
                "- Recomenda-se revisar outliers e sazonalidade.\n"
                "- Próximos passos: acompanhar KPIs semanalmente e validar qualidade dos dados."
            )
    except Exception as e:
        return f"[AI Error] {e}"
