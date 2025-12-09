import os
from groq import Groq
from config import setting
from logging_config import logger


client = Groq(api_key= setting.GROQ_API_KEY or os.getenv("GROQ_API_KEY", ""))


SYSTEM_PROMPT = """
You are an AI assistant that converts natural language questions 
into SQL queries for a SQLite database.

Database schema:
TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    gender TEXT,
    location TEXT
);

Rules:
- Return ONLY a valid SQL SELECT statement.
- Never use DELETE, UPDATE, INSERT, DROP, or other destructive operations.
- Always select from the 'customers' table.
- Always include explicit column list: customer_id, name, gender, location.
- Do NOT include backticks or triple quotes.
- Do NOT add explanation, comments, or markdown, ONLY raw SQL.
"""

def generate_sql_from_nl(user_query: str)-> str:
    logger.info(f"LLM: generating sql from query: {user_query}")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages= messages,
        temperature= 0.0
    )
    sql = response.choices[0].message.content.strip()
    logger.info(f"LLM generated SQL: {sql}")
    return sql
