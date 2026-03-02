import os
import pandas as pd
from flask import Flask, render_template, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# 讀取 Railway 環境變數
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Please set it in Railway Variables.")

engine = create_engine(DATABASE_URL)


def create_table_if_not_exists():
    """確保資料表存在"""
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bingo_stats (
            id SERIAL PRIMARY KEY,
            stat_type VARCHAR(50),
            numbers VARCHAR(50),
            count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    create_table_if_not_exists()

    selected_type = request.form.get("stat_type")

    try:
        if selected_type and selected_type != "全部":
            query = text("""
                SELECT * FROM bingo_stats
                WHERE stat_type = :stat_type
                ORDER BY created_at DESC
                LIMIT 100
            """)
            df = pd.read_sql(query, engine, params={"stat_type": selected_type})
        else:
            query = "SELECT * FROM bingo_stats ORDER BY created_at DESC LIMIT 100"
            df = pd.read_sql(query, engine)

    except Exception as e:
        return f"資料庫錯誤: {str(e)}"

    if df.empty:
        records = []
    else:
        records = df.to_dict("records")

    return render_template(
        "index.html",
        tables=records,
        selected_type=selected_type
    )


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)