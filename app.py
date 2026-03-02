from flask import Flask, render_template, request
import os
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@app.route("/", methods=["GET", "POST"])
def index():
    query = "SELECT * FROM bingo_stats"
    df = pd.read_sql(query, engine)

    results = None
    selected_date = None
    selected_category = "全部"

    if request.method == "POST":
        selected_date = request.form.get("date")
        selected_category = request.form.get("category")

        results = df[df["date"] == selected_date]

        if selected_category != "全部":
            results = results[results["category"] == selected_category]

        if results.empty:
            results = None

    categories = ["全部", "2連號", "3連號", "2同出", "3同出"]
    return render_template("index.html",
                           results=results,
                           selected_date=selected_date,
                           selected_category=selected_category,
                           categories=categories)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)