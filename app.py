from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "bingo_daily_stats_long.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
        return df
    else:
        return pd.DataFrame(columns=["日期","期數","類別","組合號碼","出現次數"])

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()
    results = None
    selected_date = None
    selected_category = "全部"

    if request.method == "POST":
        selected_date = request.form.get("date")
        selected_category = request.form.get("category")
        if selected_date:
            results = df[df["日期"] == selected_date]
            if selected_category != "全部":
                results = results[results["類別"] == selected_category]
            if results.empty:
                results = None

    categories = ["全部", "2連號", "3連號", "2同出", "3同出"]
    return render_template("index.html", results=results, selected_date=selected_date,
                           selected_category=selected_category, categories=categories)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)