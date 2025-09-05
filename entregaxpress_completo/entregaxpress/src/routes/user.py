from flask import Blueprint, jsonify, request
from src.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_bp = Blueprint('user', __name__)

def validate_cpf(cpf):
    """Validação básica de CPF"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

def validate_email(email):
    """Validação básica de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['username', 'email', 'password', 'full_name', 'phone', 'cpf', 'vehicle_type', 'vehicle_plate']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validar email
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Validar CPF
        if not validate_cpf(data['cpf']):
            return jsonify({'error': 'CPF inválido'}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Nome de usuário já existe'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        if User.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'error': 'CPF já cadastrado'}), 400
        
        # Criar novo usuário
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            full_name=data['full_name'],
            phone=data['phone'],
            cpf=data['cpf'],
            vehicle_type=data['vehicle_type'],
            vehicle_plate=data['vehicle_plate'],
            cnh=data.get('cnh', '')
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Retornar dados do usuário (sem senha)
        user_data = user.to_dict()
        user_data.pop('password', None)
        
        return jsonify({
            'message': 'Usuário registrado com sucesso',
            'user': user_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    # Redirecionar para o endpoint de registro
    return register_user()

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = user.to_dict()
    user_data.pop('password', None)  # Não retornar senha
    return jsonify(user_data)

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # Atualizar campos permitidos
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'vehicle_type' in data:
        user.vehicle_type = data['vehicle_type']
    if 'vehicle_plate' in data:
        user.vehicle_plate = data['vehicle_plate']
    if 'cnh' in data:
        user.cnh = data['cnh']
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    user_data = user.to_dict()
    user_data.pop('password', None)
    return jsonify(user_data)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
