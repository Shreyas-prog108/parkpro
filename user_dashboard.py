from flask import Blueprint,render_template,redirect,url_for,request,flash,jsonify
from flask_login import login_required,current_user
from models import db,Parkinglot,Spot,User,Reservation,Vehicle
import datetime
import re

user_dash=Blueprint('user_dash',__name__,template_folder='templates')

def validate_indian_vehicle_number(vehicle_number):
    """
    Validate Indian vehicle number format
    Format: XX00XX0000 or XX00XXX0000
    Examples: UP61ABC4376, DL01CAA1234, MH12DE1234
    """
    if not vehicle_number:
        return False, "Vehicle number is required"
    
    # Clean the input
    clean_number = vehicle_number.replace(' ', '').upper().strip()
    
    # Check length
    if len(clean_number) < 9 or len(clean_number) > 10:
        return False, "Vehicle number must be 9 or 10 characters"
    
    # Check format using regex
    pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}$'
    if not re.match(pattern, clean_number):
        return False, "Invalid format. Use format: State(2) + District(2) + Series(1-3) + Number(4)"
    
    return True, clean_number

def format_vehicle_number(vehicle_number):
    """Format vehicle number to standard format"""
    if not vehicle_number:
        return ""
    return vehicle_number.replace(' ', '').upper().strip()

@user_dash.route('/user/dash')
@login_required
def dash():
    if current_user.role=='admin':
        flash('Access Denied')
        return redirect(url_for('admin_dash.dash'))
    lot_data=[]
    lots=Parkinglot.query.all()
    for lot in lots:
        available_spots=Spot.query.filter_by(lot_id=lot.id,status='A').count()
        lot_data.append({
            'lot':lot,
            'available_spots':available_spots,
            'total_spots':Spot.query.filter_by(lot_id=lot.id).count()
        })
    active_reservations=Reservation.query.filter_by(
        user_id=current_user.id,
        leaving_timestamp=None
    ).all()
    for reservation in active_reservations:
        if reservation.vehicle:
            reservation.vehicle_number = reservation.vehicle.number
        else:
            reservation.vehicle_number = 'N/A'
    
    past_reservations=Reservation.query.filter(
        Reservation.user_id==current_user.id,
        Reservation.leaving_timestamp.isnot(None)
    ).all()
    for reservation in past_reservations:
        if reservation.vehicle:
            reservation.vehicle_number = reservation.vehicle.number
        else:
            reservation.vehicle_number = 'N/A'
    
    return render_template(
        'user_dash.html',
        lot_data=lot_data,
        active_reservations=active_reservations,
        past_reservations=past_reservations
    )

@user_dash.route('/user/book_spot',methods=['POST'])
@login_required
def book_spot():
    if current_user.role=='admin':
        return jsonify({'success': False, 'message': 'Access Denied'})
    
    lot_id = request.form.get('lot_id')
    vehicle_number = request.form.get('vehicle_number')
    
    if not lot_id or not vehicle_number:
        return jsonify({'success': False, 'message': 'Lot ID and vehicle number are required'})
    
    # Validate vehicle number format
    is_valid, result = validate_indian_vehicle_number(vehicle_number)
    if not is_valid:
        return jsonify({'success': False, 'message': f'Invalid vehicle number: {result}'})
    
    # Use the cleaned/formatted vehicle number
    vehicle_number = result
    
    try:
        lot_id = int(lot_id)
        lot = Parkinglot.query.get_or_404(lot_id)
        spot = Spot.query.filter_by(lot_id=lot.id, status='A').first()
        
        if not spot:
            return jsonify({'success': False, 'message': 'No available spots in this lot'})
        # Check if user already has an active reservation
        existing_reservation = Reservation.query.filter_by(
            user_id=current_user.id,
            leaving_timestamp=None
        ).first()
        
        if existing_reservation:
            return jsonify({'success': False, 'message': 'You already have an active parking reservation'})
        
        vehicle = Vehicle.query.filter_by(
            user_id=current_user.id,
            number=vehicle_number
        ).first()
        
        if not vehicle:
            vehicle = Vehicle(
                user_id=current_user.id,
                number=vehicle_number
            )
            db.session.add(vehicle)
            db.session.flush()
        reservation = Reservation(
            spot_id=spot.id,
            user_id=current_user.id,
            vehicle_id=vehicle.id,
            parking_timestamp=datetime.datetime.now(),
            parking_cost=lot.price_per_hour
        )
        db.session.add(reservation)
        spot.status = 'O'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Parking spot booked successfully'})
        
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid lot ID'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred while booking'})

@user_dash.route('/user/book/<int:lot_id>',methods=['POST'])
@login_required 
def book_spot_old(lot_id):
    return redirect(url_for('user_dash.dash'))

@user_dash.route('/user/release/<int:reservation_id>',methods=['POST'])
@login_required
def release_spot(reservation_id):
    reservation=Reservation.query.get_or_404(reservation_id)
    if reservation.user_id!=current_user.id:
        flash("You have not coccupied this spot.","danger")
        return redirect(url_for("user_dash.dash"))
    reservation.leaving_timestamp=datetime.datetime.now()
    reservation.spot.status='A'
    db.session.commit()
    flash("Spot released successfully.","success")
    return redirect(url_for("user_dash.dash"))

@user_dash.route('/user/summary')
@login_required
def recap():
    reservations=Reservation.query.filter_by(user_id=current_user.id).filter(Reservation.leaving_timestamp.isnot(None)).all()
    data={}
    for r in reservations:
        lot_name=r.spot.lot.prime_location_name
        duration=(r.leaving_timestamp-r.parking_timestamp).total_seconds()/60
        data[lot_name]=data.get(lot_name, 0)+duration
    return render_template("user_summary.html",chart_data=data)

@user_dash.route('/user/vehicles/json')
@login_required
def get_user_vehicles():
    """Get user's registered vehicles for auto-complete"""
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    vehicle_numbers = [vehicle.number for vehicle in vehicles]
    return jsonify({'vehicles': vehicle_numbers})
