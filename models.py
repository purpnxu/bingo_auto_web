from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BingoStats(db.Model):
    __tablename__ = "bingo_stats"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    combination = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint("date", "period", "category", "combination", name="unique_stat"),
    )