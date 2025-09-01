from flask import Blueprint, render_template, request, redirect, url_for
from src.models.user import User, db
from src.models.ride import Ride

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route('/')
def dashboard():
    users = User.query.all()
    rides = Ride.query.order_by(Ride.created_at.desc()).all()
    return render_template("admin/dashboard.html", users=users, rides=rides)

@admin_bp.route('/rides/create', methods=['POST'])
def create_ride():
    data = request.form
    ride = Ride(
        customer_id=data.get("customer_id"),
        origin_address=data.get("origin_address"),
        destination_address=data.get("destination_address"),
        item_description=data.get("item_description", ""),
        status="pending"
    )
    db.session.add(ride)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))

@admin_bp.route('/rides/<int:ride_id>/status', methods=['POST'])
def update_ride_status(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    new_status = request.form.get("status")

    valid_statuses = ['pending', 'accepted', 'in_transit', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        ride.status = new_status
        db.session.commit()
    return redirect(url_for("admin.dashboard"))
