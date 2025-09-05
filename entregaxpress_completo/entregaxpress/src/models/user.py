from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)  # moto, bicicleta, carro
    vehicle_plate = db.Column(db.String(10), nullable=False)
    cnh = db.Column(db.String(20), nullable=True)  # CNH para motos/carros
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'cpf': self.cpf,
            'vehicle_type': self.vehicle_type,
            'vehicle_plate': self.vehicle_plate,
            'cnh': self.cnh,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
