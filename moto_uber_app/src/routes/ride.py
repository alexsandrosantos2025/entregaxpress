from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.ride import Ride
from datetime import datetime
import random

ride_bp = Blueprint('ride', __name__)

@ride_bp.route('/rides', methods=['POST'])
def create_ride():
    """Criar uma nova corrida"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['customer_phone', 'origin_address', 'destination_address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Buscar ou criar cliente
        customer = User.query.filter_by(phone=data['customer_phone']).first()
        if not customer:
            customer = User(
                username=f"Cliente_{data['customer_phone'][-4:]}",
                email=f"cliente_{data['customer_phone'][-4:]}@email.com",
                phone=data['customer_phone'],
                user_type='customer'
            )
            db.session.add(customer)
            db.session.flush()  # Para obter o ID
        
        # Calcular preço estimado (simulado)
        base_price = 8.0
        distance_km = random.uniform(1.0, 10.0)  # Distância simulada
        estimated_price = base_price + (distance_km * 1.5)
        estimated_time = int(distance_km * 3 + random.uniform(5, 15))  # Tempo simulado
        
        # Criar nova corrida
        ride = Ride(
            customer_id=customer.id,
            origin_address=data['origin_address'],
            destination_address=data['destination_address'],
            item_description=data.get('item_description', ''),
            estimated_price=round(estimated_price, 2),
            distance_km=round(distance_km, 1),
            estimated_time_minutes=estimated_time,
            # Coordenadas simuladas (São Paulo)
            origin_lat=-23.5505 + random.uniform(-0.1, 0.1),
            origin_lng=-46.6333 + random.uniform(-0.1, 0.1),
            destination_lat=-23.5505 + random.uniform(-0.1, 0.1),
            destination_lng=-46.6333 + random.uniform(-0.1, 0.1)
        )
        
        db.session.add(ride)
        db.session.commit()
        
        return jsonify({
            'message': 'Corrida criada com sucesso',
            'ride': ride.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/rides/pending', methods=['GET'])
def get_pending_rides():
    """Obter corridas pendentes para motoboys"""
    try:
        pending_rides = Ride.query.filter_by(status='pending').order_by(Ride.created_at.desc()).all()
        return jsonify({
            'rides': [ride.to_dict() for ride in pending_rides]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/rides/<int:ride_id>/accept', methods=['POST'])
def accept_ride(ride_id):
    """Aceitar uma corrida"""
    try:
        data = request.get_json()
        driver_phone = data.get('driver_phone')
        
        if not driver_phone:
            return jsonify({'error': 'Telefone do motoboy é obrigatório'}), 400
        
        # Buscar ou criar motoboy
        driver = User.query.filter_by(phone=driver_phone, user_type='driver').first()
        if not driver:
            driver = User(
                username=f"Motoboy_{driver_phone[-4:]}",
                email=f"motoboy_{driver_phone[-4:]}@email.com",
                phone=driver_phone,
                user_type='driver',
                is_online=True
            )
            db.session.add(driver)
            db.session.flush()
        
        # Buscar corrida
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Corrida não encontrada'}), 404
        
        if ride.status != 'pending':
            return jsonify({'error': 'Corrida não está disponível'}), 400
        
        # Aceitar corrida
        ride.driver_id = driver.id
        ride.status = 'accepted'
        ride.accepted_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Corrida aceita com sucesso',
            'ride': ride.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/rides/<int:ride_id>/status', methods=['PUT'])
def update_ride_status(ride_id):
    """Atualizar status da corrida"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        valid_statuses = ['accepted', 'picked_up', 'in_transit', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({'error': 'Status inválido'}), 400
        
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Corrida não encontrada'}), 404
        
        # Atualizar status e timestamp correspondente
        ride.status = new_status
        
        if new_status == 'picked_up':
            ride.picked_up_at = datetime.utcnow()
        elif new_status == 'delivered':
            ride.delivered_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Status atualizado com sucesso',
            'ride': ride.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/rides/<int:ride_id>', methods=['GET'])
def get_ride(ride_id):
    """Obter detalhes de uma corrida específica"""
    try:
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Corrida não encontrada'}), 404
        
        return jsonify({'ride': ride.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/rides', methods=['GET'])
def get_all_rides():
    """Obter todas as corridas (para admin)"""
    try:
        rides = Ride.query.order_by(Ride.created_at.desc()).all()
        return jsonify({
            'rides': [ride.to_dict() for ride in rides]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/drivers/online', methods=['GET'])
def get_online_drivers():
    """Obter motoboys online"""
    try:
        online_drivers = User.query.filter_by(user_type='driver', is_online=True).all()
        return jsonify({
            'drivers': [driver.to_dict() for driver in online_drivers]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ride_bp.route('/drivers/<driver_phone>/status', methods=['PUT'])
def update_driver_status(driver_phone):
    """Atualizar status online/offline do motoboy"""
    try:
        data = request.get_json()
        is_online = data.get('is_online', False)
        
        driver = User.query.filter_by(phone=driver_phone, user_type='driver').first()
        if not driver:
            return jsonify({'error': 'Motoboy não encontrado'}), 404
        
        driver.is_online = is_online
        db.session.commit()
        
        return jsonify({
            'message': f'Status atualizado para {"online" if is_online else "offline"}',
            'driver': driver.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

