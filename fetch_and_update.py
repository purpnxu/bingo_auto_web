import pandas as pd
import datetime
from flask import Flask
from models import db, BingoStats
import os

# Flask app context for SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")  # PostgreSQL URI from Railway
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def fetch_latest_data():
    """替換成你的真實抓資料或 API 邏輯"""
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
                db.session.rollback()  # 已存在就跳過
        print(f"{datetime.datetime.now()} - DB 更新完成，共 {len(df)} 筆資料")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 第一次自動建表
    update_db()