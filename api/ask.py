
from flask import Flask, request, jsonify
from llm.gemini_agent import generate_sql_query
import sqlite3
import os
from dotenv import load_dotenv
from visualization.plotter import try_generate_plot

load_dotenv()
app = Flask(__name__)
DATABASE = os.path.join("database", "ecommerce.db")

@app.route("/ask")
def ask():
    question = request.args.get("q")
    if not question:
        return jsonify({"error": "Missing 'q' query parameter"}), 400

    # Step 1: Get SQL from LLM
    sql_query = generate_sql_query(question)
    if not sql_query:
        return jsonify({"error": "Failed to generate SQL query"}), 500

    try:
        # Step 2: Query database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        # Step 3: Format response
        results = [dict(zip(columns, row)) for row in rows]

        # Optional: Try to generate a graph
        graph_url = try_generate_plot(columns, rows, question)

        return jsonify({
            "question": question,
            "sql": sql_query,
            "results": results,
            "graph": graph_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
