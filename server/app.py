from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)  # Allow NULL for image
    price = db.Column(db.Float, nullable=True)  # Allow NULL for price

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': self.price
        }

@app.route('/plants', methods=['GET'])
def get_plants():
    """Get all plants."""
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

@app.route('/plants', methods=['POST'])
def create_plant():
    """Create a new plant record."""
    data = request.json
    new_plant = Plant(
        name=data['name'],
        image=data.get('image'),  # Use get to allow None
        price=data.get('price')   # Use get to allow None
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant_by_id(id):
    """Get a plant by ID."""
    plant = Plant.query.get_or_404(id)
    return jsonify(plant.to_dict()), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the tables are created
    app.run(debug=True)
