from flask import Flask, render_template, request
from models import db, BingoStats
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    selected_date = None
    selected_category = "全部"

    if request.method == "POST":
        selected_date = request.form.get("date")
        selected_category = request.form.get("category")
        
        query = BingoStats.query
        if selected_date:
            query = query.filter_by(date=selected_date)
        if selected_category and selected_category != "全部":
            query = query.filter_by(category=selected_category)
        results = query.order_by(BingoStats.created_at.desc()).all()
    
    categories = ["全部", "2連號", "3連號", "2同出", "3同出"]
    return render_template("index.html", results=results, selected_date=selected_date,
                           selected_category=selected_category, categories=categories)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 確保表存在
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)