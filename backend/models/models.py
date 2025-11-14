from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'address': self.address,
            'pincode': self.pincode,
            'email': self.email,
            'role': self.role
        }

class Parking_lot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parking_spot = db.relationship('Parking_spot', backref='parking_lot', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'location': self.location,
            'pincode': self.pincode,
            'capacity': self.capacity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
class Parking_spot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id', ondelete="SET NULL"), nullable=False)
    # spot_number = db.Column(db.String(50), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    reservation = db.relationship('Reservation', backref='parking_spot', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'is_occupied': self.is_occupied
        }
        

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id', ondelete="SET NULL"), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    parking_time = db.Column(db.DateTime, nullable=False)
    leaving_time = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'spot_id': self.spot_id,
            'vehicle_number': self.vehicle_number,
            'parking_time': self.parking_time.isoformat(),
            'leaving_time': self.leaving_time.isoformat() if self.leaving_time else None,
            'parking_cost': self.parking_cost
        }