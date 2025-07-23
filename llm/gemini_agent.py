# llm/gemini_agent.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import traceback

# Load .env
load_dotenv()

# ✅ Get API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is not set. Please check your .env file.")

# ✅ Fix: Correct model name
llm = ChatGoogleGenerativeAI(model="models/gemini-pro", temperature=0.3, google_api_key=GOOGLE_API_KEY)

template = """
You are an expert SQL assistant. Convert the following user question into a valid SQL query.
The database has 3 tables: 'ad_sales', 'total_sales', and 'eligibility'.
Only generate SQL — do not include explanations.

Question: {question}

SQL Query:
"""

prompt = PromptTemplate(template=template, input_variables=["question"])
sql_chain = LLMChain(llm=llm, prompt=prompt)

def generate_sql_query(question):
    try:
        result = sql_chain.run(question)
        return result.strip().strip("```sql").strip("```").strip()
    except Exception as e:
        print("❌ LLM Error:", e)
        traceback.print_exc()
        return None
