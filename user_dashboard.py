from flask import Blueprint,render_template,redirect,url_for,request,flash,jsonify
from flask_login import login_required,current_user
from models import db,Parkinglot,Spot,User,Reservation,Vehicle
import datetime

user_dash=Blueprint('user_dash',__name__,template_folder='templates')

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
    
    try:
        lot_id = int(lot_id)
        lot = Parkinglot.query.get_or_404(lot_id)
        spot = Spot.query.filter_by(lot_id=lot.id, status='A').first()
        
        if not spot:
            return jsonify({'success': False, 'message': 'No available spots in this lot'})
        existing_reservation = Reservation.query.filter_by(
            user_id=current_user.id,
            leaving_timestamp=None
        ).first()
        vehicle = Vehicle.query.filter_by(
            user_id=current_user.id,
            number=vehicle_number.upper().strip()
        ).first()
        
        if not vehicle:
            vehicle = Vehicle(
                user_id=current_user.id,
                number=vehicle_number.upper().strip()
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
