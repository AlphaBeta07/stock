import os
from flask import Flask, request, jsonify, render_template
from models import db, Perfume

app = Flask(__name__)

# Configure database from Render's DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfumes', methods=['GET'])
def get_perfumes():
    perfumes = Perfume.query.all()
    return jsonify([p.to_dict() for p in perfumes])

@app.route('/perfume', methods=['POST'])
def add_perfume():
    data = request.json
    perfume = Perfume(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(perfume)
    db.session.commit()
    return jsonify({"message": "Perfume added successfully"})

@app.route('/perfume/<int:id>', methods=['PUT'])
def update_perfume(id):
    perfume = Perfume.query.get_or_404(id)
    data = request.json
    perfume.name = data.get('name', perfume.name)
    perfume.category = data.get('category', perfume.category)
    perfume.price = data.get('price', perfume.price)
    perfume.quantity = data.get('quantity', perfume.quantity)
    db.session.commit()
    return jsonify({"message": "Perfume updated successfully"})

@app.route('/perfume/<int:id>', methods=['DELETE'])
def delete_perfume(id):
    perfume = Perfume.query.get_or_404(id)
    db.session.delete(perfume)
    db.session.commit()
    return jsonify({"message": "Perfume deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
