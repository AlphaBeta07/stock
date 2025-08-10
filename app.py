from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, Perfume
import os

app = Flask(__name__)
CORS(app)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///perfumes.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_perfume():
    data = request.get_json()
    new_perfume = Perfume(
        name=data["name"],
        category=data["category"],
        price=float(data["price"]),
        quantity=int(data["quantity"])
    )
    db.session.add(new_perfume)
    db.session.commit()
    return jsonify({"message": "Perfume added successfully!"})

@app.route("/get", methods=["GET"])
def get_perfumes():
    perfumes = Perfume.query.all()
    return jsonify([p.to_dict() for p in perfumes])

@app.route("/update", methods=["POST"])
def update_perfume():
    data = request.get_json()
    perfume = Perfume.query.get(data["id"])
    if perfume:
        perfume.name = data["name"]
        perfume.category = data["category"]
        perfume.price = float(data["price"])
        perfume.quantity = int(data["quantity"])
        db.session.commit()
        return jsonify({"message": "Perfume updated successfully!"})
    return jsonify({"error": "Perfume not found"}), 404

@app.route("/delete", methods=["POST"])
def delete_perfume():
    data = request.get_json()
    perfume = Perfume.query.get(data["id"])
    if perfume:
        db.session.delete(perfume)
        db.session.commit()
        return jsonify({"message": "Perfume deleted successfully!"})
    return jsonify({"error": "Perfume not found"}), 404

@app.route("/total", methods=["GET"])
def get_total():
    perfumes = Perfume.query.all()
    total_value = sum(p.price * p.quantity for p in perfumes)
    return jsonify({"total": total_value})

if __name__ == "__main__":
    app.run(debug=True)
