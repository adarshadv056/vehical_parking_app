import io
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from flask import Flask, jsonify, request, send_file, Blueprint
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from celery.result import AsyncResult
from applications.task import *
from sqlalchemy.orm import joinedload
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app, send_from_directory
from app import cache
from models.models import *


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"message": "Welcome to the Parking Management System API!"})


@app.route("/register", methods=["GET", "POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    username = request.json.get("username")
    address = request.json.get("address")
    pincode = request.json.get("pincode")

    if user.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = user(
        email=email,
        password=generate_password_hash(password),
        username=username,
        address=address,
        pincode=pincode,
        role="user",
    )
    db.session.add(new_user)
    db.session.commit()
    cache.delete("all_users")
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user_data = user.query.filter_by(email=email).first()
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    if not check_password_hash(user_data.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user_data.id),
        additional_claims={"role": user_data.role, "username": user_data.username},
    )

    return jsonify({"access_token": access_token}), 200


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return jsonify({"message": "Logout endpoint - please implement logout logic here."})


@app.route("/user", methods=["GET", "POST"])
@jwt_required()
def user_dashboard():
    user_info = get_jwt()
    return jsonify({"message": f"Welcome, {user_info['username']}!"})


@app.route("/admin", methods=["GET", "POST"])
@jwt_required()
def admin_dashboard():
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403
    return jsonify({"message": "Welcome to the Admin Dashboard!"}), 200


@app.route("/admin/add_lot", methods=["GET", "POST"])
@jwt_required()
def add_parking_lot():
    cache.delete('get_parking_lots')
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    name = request.json.get("name")
    price = request.json.get("price")
    location = request.json.get("location")
    pincode = request.json.get("pincode")
    capacity = request.json.get("capacity")

    if Parking_lot.query.filter_by(name=name).first():
        return jsonify({"message": "Parking lot already exists"}), 400

    new_lot = Parking_lot(
        name=name,
        price=float(price),
        location=location,
        pincode=pincode,
        capacity=int(capacity),
    )

    db.session.add(new_lot)
    db.session.commit()
    
    for i in range(capacity):
        spot = Parking_spot(lot_id=new_lot.id, is_occupied=False)
        db.session.add(spot)

    db.session.commit()
    # result = daily_reminder.delay()
    return jsonify({"message": "Parking lot added successfully"}), 201

@app.route("/admin/get_lots", methods=["GET"])
@cache.cached(timeout=60, key_prefix='get_parking_lots')
@jwt_required()
def get_parking_lots():
    print("Fetching data from DB...")
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    parking_lots = Parking_lot.query.all()
    lots_data = []
    for lot in parking_lots:
        parking_spots = Parking_spot.query.filter_by(lot_id=lot.id).all()
        occupied_spots = sum(1 for spot in parking_spots if spot.is_occupied)
        lot_dict = lot.to_dict()
        lot_dict["spots"] = [spot.to_dict() for spot in parking_spots]
        lot_dict["occupied_spots"] = occupied_spots
        lot_dict["available_spots"] = int(lot.capacity) - occupied_spots
        lots_data.append(lot_dict)
    return jsonify({"parking_lots": lots_data, "total_lots": len(lots_data)}), 200

@app.route("/admin/get_lot/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_parking_lot(lot_id):
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    lot = Parking_lot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    return jsonify({"parking_lot": lot.to_dict()}), 200

@app.route("/admin/delete_lot/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_lot(lot_id):
    cache.delete('get_parking_lots')
    lot = Parking_lot.query.get(lot_id)
    spots = Parking_spot.query.filter_by(lot_id=lot_id).all()
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    for spot in spots:
        if spot.is_occupied:
            return jsonify({"message": "Can't delete lot with occupied spots"}), 400
        db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()
    return jsonify({"message": "Parking lot deleted successfully"}), 200

@app.route("/admin/edit_lot/<int:lot_id>", methods=["PUT"])
@jwt_required()
def edit_parking_lot(lot_id):
    cache.delete('get_parking_lots')
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    lot = Parking_lot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    name = request.json.get("name")
    price = request.json.get("price")
    location = request.json.get("location")
    pincode = request.json.get("pincode")
    capacity = request.json.get("capacity")

    lot.name = name
    lot.price = float(price)
    lot.location = location
    lot.pincode = pincode
    lot.capacity = int(capacity)
    
    old_capacity = len(lot.parking_spot)
    occupied_spots = Parking_spot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
    if lot.capacity < occupied_spots:
        return jsonify({"message": "New capacity cannot be less than occupied spots"}), 400
    if lot.capacity > old_capacity:
        for i in range(old_capacity, lot.capacity):
            new_spot = Parking_spot(lot_id=lot.id, is_occupied=False)
            db.session.add(new_spot)
    else:
        if lot.capacity < old_capacity:
            spots_to_remove = old_capacity - lot.capacity
            spots = Parking_spot.query.filter_by(lot_id=lot.id, is_occupied=False).limit(spots_to_remove).all()
            for spot in spots:
                db.session.delete(spot)

    db.session.commit()
    return jsonify({"message": "Parking lot updated successfully"}), 200

@app.route("/admin/get_spot/<int:spot_id>", methods=["GET", "POST"])
@jwt_required()
def get_parking_spot(spot_id):
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    spot = Parking_spot.query.get(spot_id)
    if not spot:
        return jsonify({"message": "Parking spot not found"}), 404

    if request.method == "POST":
        return jsonify({"message": "Parking spot closed successfully"}), 200

    return jsonify({"spot": spot.to_dict()}), 200

@app.route("/admin/delete_spot/<int:spot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_spot(spot_id):
    cache.delete('get_parking_lots')
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    spot = Parking_spot.query.get(spot_id)
    if not spot:
        return jsonify({"message": "Parking spot not found"}), 404

    if spot.is_occupied:
        return jsonify({"message": "Cannot delete occupied parking spot"}), 400

    lot = Parking_lot.query.get(spot.lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404
    
    lot.capacity -= 1
    
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"message": "Parking spot deleted successfully"}), 200

@app.route("/admin/get_reservations/<int:spot_id>", methods=["GET"])
@jwt_required()
def get_reservations(spot_id):
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    reservation = Reservation.query.filter_by(spot_id=spot_id, leaving_time=None).first()
    if not reservation:
        return jsonify({"message": "No active reservation found for this spot"}), 404

    return jsonify({"reservation": reservation.to_dict()}), 200


@app.route("/admin/users", methods=["GET"])
@cache.cached(timeout=120, key_prefix='all_users')
@jwt_required()
def get_users():
    print("Fetching users from DB...")
    user_info = get_jwt()
    if user_info["role"] != "admin":
        return jsonify({"message": "Access forbidden: Admins only!"}), 403

    users = user.query.filter_by(role="user").all()
    users_data = [u.to_dict() for u in users]
    
    return jsonify({"users": users_data, "total_users": len(users_data)}), 200

@app.route('/admin/revenue_chart')
@cache.cached(timeout=120, key_prefix='revenue_chart')
def revenue_chart():
    reservations = Reservation.query.all()
    
    spot_map = {spot.id: spot.lot_id for spot in Parking_spot.query.all()}
    
    revenue_by_lot = {}
    for res in reservations:
        lot_id = spot_map.get(res.spot_id)
        if lot_id:
            revenue_by_lot[lot_id] = revenue_by_lot.get(lot_id, 0) + res.parking_cost

    plt.figure(figsize=(6, 4))
    plt.bar([str(k) for k in revenue_by_lot.keys()], revenue_by_lot.values(), color='green')
    plt.xlabel("Lot ID")
    plt.ylabel("Revenue (₹)")
    plt.title("Revenue by Parking Lot")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

@app.route('/user/lot_distribution_chart')
@jwt_required()
def lot_distribution_chart():
    user_id = get_jwt_identity()
    user_reservations = Reservation.query.filter_by(user_id=user_id).all()

    spot_map = {spot.id: spot.lot_id for spot in Parking_spot.query.all()}
    lot_map = {lot.id: lot.name for lot in Parking_lot.query.all()}

    lot_count = {}
    for res in user_reservations:
        lot_id = spot_map.get(res.spot_id)
        if lot_id:
            lot_name = lot_map.get(lot_id, f"Lot {lot_id}")
            lot_count[lot_name] = lot_count.get(lot_name, 0) + 1

    plt.figure(figsize=(5, 5))
    plt.pie(lot_count.values(), labels=lot_count.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Where You Parked the Most")
    plt.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')



@app.route("/user/search_lot", methods=["GET"])
@jwt_required()
def search_parking_lot():
    user_info = get_jwt()
    if user_info["role"] != "user":
        return jsonify({"message": "Access forbidden: Users only!"}), 403

    query = request.args.get("query", "")
    if not query:
        return jsonify({"message": "Search query is required"}), 400
    
    parking_lots = Parking_lot.query.filter(
        (Parking_lot.location.ilike(f"%{query}%")) | (Parking_lot.pincode.ilike(f"%{query}%")) | (Parking_lot.name.ilike(f"%{query}%"))
    ).all()
    
    lots_data = []
    for lot in parking_lots:
        total_spots = Parking_spot.query.filter_by(lot_id=lot.id).count()
        occupied_spots = Parking_spot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
        available_spots = total_spots - occupied_spots
        
        lot_dict = lot.to_dict()
        
        lot_dict["total_spots"] = total_spots
        lot_dict["occupied_spots"] = occupied_spots
        lot_dict["available_spots"] = available_spots
        lot_dict["availability_text"] = f"{available_spots}/{total_spots} available"
        
        lots_data.append(lot_dict)
    return jsonify({"parking_lots": lots_data}), 200

@app.route("/user/get_first_spot/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_first_parking_spot(lot_id):
    user_info = get_jwt()
    if user_info["role"] != "user":
        return jsonify({"message": "Access forbidden: Users only!"}), 403

    spot = Parking_spot.query.filter_by(lot_id=lot_id, is_occupied=False).first()
    if not spot:
        return jsonify({"message": "No available parking spots found"}), 404

    return jsonify({"parking_spot": spot.to_dict()}), 200


@app.route("/user/book_spot/<int:spot_id>", methods=["POST"])
@jwt_required()
def book_parking_spot(spot_id):
    cache.delete('revenue_chart')
    cache.delete('get_parking_lots')
    user_info = get_jwt()
    if user_info["role"] != "user":
        return jsonify({"message": "Access forbidden: Users only!"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    spot = Parking_spot.query.get(spot_id)
    spot.is_occupied = True
    
    user_id = get_jwt_identity()
    vehicle_no = data.get("vehicleNo")
    parking_lot = Parking_lot.query.get(spot.lot_id)
    
    new_reservation = Reservation(
        user_id=user_id,
        spot_id=spot.id,
        vehicle_number=vehicle_no,
        parking_time=datetime.now(),
        parking_cost=parking_lot.price
    )
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Parking spot booked successfully"}), 200

@app.route("/user/get_history", methods=["GET"])
@jwt_required()
def get_parking_history():
    user_info = get_jwt()
    if user_info["role"] != "user":
        return jsonify({"message": "Access forbidden: Users only!"}), 403

    user_id = get_jwt_identity()
    reservation = Reservation.query.filter_by(user_id=user_id).all()
    history_data = []
    
    for res in reservation:
        spot = Parking_spot.query.get(res.spot_id)
        lot = Parking_lot.query.get(spot.lot_id)
        
        if res.leaving_time is None:
            time_diff = datetime.now() - res.parking_time
            hours_parked = time_diff.total_seconds() / 3600
            
            if hours_parked < 1:
                billable_hours = 1
            else:
                billable_hours = int(hours_parked) + (1 if hours_parked % 1 > 0 else 0)
            current_cost = billable_hours * lot.price
            res.parking_cost = current_cost
            db.session.commit()
        else:
            current_cost = res.parking_cost
        
        res_dict = res.to_dict()
        res_dict["location"] = lot.location
        res_dict["lot_name"] = lot.name
        res_dict["parking_cost"] = current_cost
        res_dict["hourly_rate"] = lot.price
        history_data.append(res_dict)
    return jsonify({"history": history_data}), 200

@app.route("/user/park_out/<int:history_id>", methods=["POST"])
@jwt_required()
def park_out(history_id):
    cache.delete('revenue_chart')
    cache.delete('get_parking_lots')
    user_info = get_jwt()
    if user_info["role"] != "user":
        return jsonify({"message": "Access forbidden: Users only!"}), 403

    reservation = Reservation.query.get(history_id)
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    
    if reservation.leaving_time is not None:
        return jsonify({"message": "Vehicle already checked out"}), 400
    
    reservation.leaving_time = datetime.now()

    spot = Parking_spot.query.get(reservation.spot_id)
    if not spot:
        return jsonify({"message": "Parking spot not found"}), 404
    spot.is_occupied = False
    lot = Parking_lot.query.get(spot.lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    db.session.commit()
    return jsonify({"message": "Vehicle checked out successfully"}), 200


@app.route('/export_csv_result/<int:user_id>',methods=["GET"])
def export_csv_result(user_id):
    result = csv_report.delay(user_id)
    return jsonify({
        "id": result.id,
        "result":result.result,
    })
    
@app.route('/csv_download/<id>')
def csv_download(id):
    result = AsyncResult(id)
    return send_from_directory('static',result.result)