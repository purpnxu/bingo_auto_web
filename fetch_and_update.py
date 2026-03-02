import os
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

engine = create_engine(DATABASE_URL)

def create_table_if_not_exists():
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

def insert_dummy_data():
    data = [
        {"stat_type": "2連號", "numbers": "2,3", "count": 139},
        {"stat_type": "2連號", "numbers": "1,2", "count": 87},
        {"stat_type": "3連號", "numbers": "2,3,4", "count": 77},
    ]

    df = pd.DataFrame(data)
    df.to_sql("bingo_stats", engine, if_exists="append", index=False)

if __name__ == "__main__":
    create_table_if_not_exists()
    insert_dummy_data()
    print("資料表建立並寫入完成")