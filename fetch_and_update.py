import os
import pandas as pd
from sqlalchemy import create_engine, text
import datetime

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def create_table():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bingo_stats (
                id SERIAL PRIMARY KEY,
                date VARCHAR(20),
                period INTEGER,
                category VARCHAR(20),
                numbers VARCHAR(50),
                count INTEGER
            );
        """))
        conn.commit()

def fetch_latest_data():
    # ⚠️ 這裡替換成你真正抓資料邏輯
    today = datetime.date.today().strftime("%Y-%m-%d")
    data = {
        "date": [today]*2,
        "period": [1, 2],
        "category": ["2連號", "3連號"],
        "numbers": ["01 02", "03 04 05"],
        "count": [10, 5],
    }
    return pd.DataFrame(data)

def update_db():
    create_table()
    df = fetch_latest_data()

    with engine.connect() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO bingo_stats (date, period, category, numbers, count)
                VALUES (:date, :period, :category, :numbers, :count)
            """), {
                "date": row["date"],
                "period": row["period"],
                "category": row["category"],
                "numbers": row["numbers"],
                "count": row["count"]
            })
        conn.commit()

    print("資料庫更新完成")

if __name__ == "__main__":
    update_db()