
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import re

# Load Together AI Key
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model_name="meta-llama/Llama-3-8b-chat-hf",  # Or any supported Together model
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.0
)

#prompt_template = PromptTemplate(
  #  input_variables=["question"],
 #   template="""
#You are an AI that converts user questions into SQL queries for an e-commerce database.

#Use the following schema:
#Table: total_sales(date, item_id, total_sales, total_units_ordered)
#Table: ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
#Table: eligibility(eligibility_datetime_utc, item_id, eligibility, message)

#ONLY return the SQL inside triple backticks like this:
#```sql
#SELECT * FROM table_name;

#```
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
You are an AI that converts user questions into SQL queries for an e-commerce database.

Use the following schema:
Table: total_sales(date, item_id, total_sales, total_units_ordered)
Table: ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
Table: eligibility(eligibility_datetime_utc, item_id, eligibility, message)

Use only the columns provided in the schema.

Note:
- Return on Ad Spend (RoAS) = ad_sales / ad_spend

ONLY return the SQL inside triple backticks like this:
```sql
SELECT * FROM table_name;


Do not include explanations or comments. Return only the SQL.

Question: {question}
SQL:
"""
)

chain = LLMChain(llm=llm, prompt=prompt_template)

#def extract_sql_from_response(response_text):
 #   match = re.search(r"```sql(.*?)```", response_text, re.DOTALL | re.IGNORECASE)
  #  if match:
   #     return match.group(1).strip()
    #return response_text.strip()
def extract_sql_from_response(response_text):
    # Remove triple backticks and optional 'sql' language tag
    cleaned = re.sub(r"```sql|```", "", response_text, flags=re.IGNORECASE).strip()
    return cleaned

def generate_sql_query(question):
    try:
        raw_response = chain.run(question)
        return extract_sql_from_response(raw_response)
    except Exception as e:
        print("Error in Together LLM:", e)
        return None

