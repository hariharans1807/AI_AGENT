import streamlit as st
import sqlite3
from llm.openai_agent import generate_sql_query  # Ensure this is implemented

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI E-commerce Analyst", layout="centered")

# --- Custom CSS for background and UI styling ---
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://www.greenhonchos.com/wp-content/uploads/2024/11/Mask-Group-108.jpg');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.93);
            padding: 2rem;
            border-radius: 1rem;
            max-width: 800px;
            margin: 2rem auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        h1 {
            color: #1f4e79;
        }
        .stButton>button {
            background-color: #1f4e79;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
        }
        .stButton>button:hover {
            background-color: #14406e;
        }
    </style>
""", unsafe_allow_html=True)


# --- Start Main Container ---
st.markdown("<div class='main'>", unsafe_allow_html=True)

# --- Title and Description ---
st.markdown("""
    <div style='text-align: center;'>
        <h1>📊 AI E-commerce Analyst</h1>
        <p style='font-size: 1.2rem;'>Ask questions about your e-commerce sales, ad performance, and product eligibility.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Ask Question UI ---
question = st.text_input("💬 Ask a question:", placeholder="e.g., What are the top selling items?")

if st.button("🧠 Generate SQL & Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating SQL using LLM..."):
            sql_query = generate_sql_query(question)

        st.code(sql_query, language="sql")

        try:
            # ✅ Create connection inside the button press (avoids threading error)
            conn = sqlite3.connect("ecom_data.db")
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()

            st.success("✅ Query executed successfully!")

            if rows:
                st.dataframe([dict(zip(columns, row)) for row in rows])
            else:
                st.info("Query executed, but returned no results.")

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

# --- Footer ---
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 0.9rem; color: #555;'>
        Built with ❤️ using Streamlit and LangChain | © 2025
    </div>
""", unsafe_allow_html=True)

# --- Close Main Container ---
st.markdown("</div>", unsafe_allow_html=True)
