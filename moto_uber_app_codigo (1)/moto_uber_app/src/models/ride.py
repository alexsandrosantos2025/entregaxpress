from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(20), nullable=False, default='customer')  # customer, driver
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'is_online': self.is_online,
            'created_at': self.created_at.isoformat()
        }

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Endereços
    origin_address = db.Column(db.String(200), nullable=False)
    destination_address = db.Column(db.String(200), nullable=False)
    
    # Coordenadas (simuladas)
    origin_lat = db.Column(db.Float, nullable=True)
    origin_lng = db.Column(db.Float, nullable=True)
    destination_lat = db.Column(db.Float, nullable=True)
    destination_lng = db.Column(db.Float, nullable=True)
    
    # Detalhes da corrida
    item_description = db.Column(db.String(200), nullable=True)
    estimated_price = db.Column(db.Float, nullable=False, default=0.0)
    distance_km = db.Column(db.Float, nullable=True)
    estimated_time_minutes = db.Column(db.Integer, nullable=True)
    
    # Status da corrida
    status = db.Column(db.String(20), nullable=False, default='pending')
    # pending, accepted, picked_up, in_transit, delivered, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)
    picked_up_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamentos
    customer = db.relationship('User', foreign_keys=[customer_id], backref='customer_rides')
    driver = db.relationship('User', foreign_keys=[driver_id], backref='driver_rides')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'driver_id': self.driver_id,
            'origin_address': self.origin_address,
            'destination_address': self.destination_address,
            'origin_lat': self.origin_lat,
            'origin_lng': self.origin_lng,
            'destination_lat': self.destination_lat,
            'destination_lng': self.destination_lng,
            'item_description': self.item_description,
            'estimated_price': self.estimated_price,
            'distance_km': self.distance_km,
            'estimated_time_minutes': self.estimated_time_minutes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'picked_up_at': self.picked_up_at.isoformat() if self.picked_up_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'driver': self.driver.to_dict() if self.driver else None
        }

