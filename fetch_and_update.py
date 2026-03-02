import pandas as pd
import datetime
from flask import Flask
from models import db, BingoStats
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set!")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def fetch_latest_data():
    today = datetime.date.today().strftime("%Y-%m-%d")
    data = {
        "date": [today]*3,
        "period": [1, 2, 3],
        "category": ["2連號", "3連號", "2同出"],
        "combination": ["01 02", "03 04 05", "06 07"],
        "count": [10, 5, 8],
    }
    df = pd.DataFrame(data)
    return df

def update_db():
    df = fetch_latest_data()
    with app.app_context():
        for _, row in df.iterrows():
            stat = BingoStats(
                date=row["date"],
                period=row["period"],
                category=row["category"],
                combination=row["combination"],
                count=row["count"]
            )
            try:
                db.session.add(stat)
                db.session.commit()
            except Exception:
                db.session.rollback()
        print(f"{datetime.datetime.now()} - DB 更新完成，共 {len(df)} 筆資料")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    update_db()