from flask import Blueprint,render_template,redirect,url_for,request,flash,jsonify
from flask_login import login_required,current_user
from models import db,Parkinglot,Spot,User,Reservation,Vehicle
import json

admin_dash=Blueprint('admin_dash',__name__,template_folder='templates')

@admin_dash.route('/admin/dash')
@login_required
def dash():
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    lots=Parkinglot.query.all()
    lot_data=[]
    for lot in lots:
        total=Spot.query.filter_by(lot_id=lot.id).count()
        available=Spot.query.filter_by(lot_id=lot.id,status='A').count()
        occupieds=Spot.query.filter_by(lot_id=lot.id,status='O').count()
        lot_data.append({
            'lot': lot,
            'total_spots': total,
            'available_spots': available,
            'occupied_spots': occupieds
        })
    users=User.query.filter(User.role!='admin').all()
    return render_template('admin_dash.html',lot_data=lot_data,users=users)

@admin_dash.route('/admin/create_lot',methods=['GET','POST'])
@login_required
def create_lot():
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    if request.method=='POST':
        name=request.form['name']
        price_per_hour=float(request.form['price_per_hour'])
        address=request.form['address']
        pin_code=request.form['pin_code']
        max_spots=int(request.form['max_spots'])
        try:
            new_lot=Parkinglot(prime_location_name=name,price_per_hour=price_per_hour,address=address,pin_code=pin_code,number_of_spots=max_spots)
            db.session.add(new_lot)
            db.session.flush()  # Get the lot ID
            
            # Add spots one by one to avoid batch insert issues
            for i in range(max_spots):
                spot=Spot(lot_id=new_lot.id,status='A')
                db.session.add(spot)
                db.session.flush()  # Flush each spot individually
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating parking lot: {str(e)}', 'error')
            return redirect(url_for('admin_dash.create_lot'))
        flash('Lot Created Successfully!')
        return redirect(url_for('admin_dash.dash'))
    return render_template('create_lot.html')

@admin_dash.route('/admin/lot/<int:lot_id>/spots')
@login_required
def view_lot_spots(lot_id):
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    lot=Parkinglot.query.get_or_404(lot_id)
    spots=Spot.query.filter_by(lot_id=lot_id).all()
    spot_data=[]
    for spot in spots:
        spot_info={
            'id':spot.id,
            'status':spot.status,
            'user_name': None,
            'vehicle_number': None,
            'parking_time': None
        }
        if spot.status=='O':
            reservation=Reservation.query.filter_by(spot_id=spot.id,leaving_timestamp=None).first()
            if reservation:
                user = User.query.get(reservation.user_id)
                spot_info['user_name']=user.name
                spot_info['parking_time']=reservation.parking_timestamp
                if reservation.vehicle_id:
                    from models import Vehicle
                    vehicle=Vehicle.query.get(reservation.vehicle_id)
                    spot_info['vehicle_number']=vehicle.number if vehicle else 'N/A'
        spot_data.append(spot_info)
    return render_template('view_parking_status.html', lot=lot, spots=spot_data)

@admin_dash.route('/admin/lot/<int:lot_id>/spots/json')
@login_required
def view_lot(lot_id):
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    lot=Parkinglot.query.get_or_404(lot_id)
    spots=Spot.query.filter_by(lot_id=lot_id).all()
    total_spots=len(spots)
    available_spots=sum(1 for spot in spots if spot.status =='A')
    occupied_spots=sum(1 for spot in spots if spot.status =='O')
    spot_data=[]
    for spot in spots:
        spot_info={
            'id':spot.id,
            'status':spot.status
        }
        if spot.status=='O':
            reservation=Reservation.query.filter_by(spot_id=spot.id,leaving_timestamp=None).first()
            if reservation:
                user=User.query.get(reservation.user_id)
                spot_info['user_name']=user.name
        else:
            spot_info['user_name']=None
        spot_data.append(spot_info)
    return jsonify({
        'lot_name':lot.prime_location_name,
        'total_spots':total_spots,
        'available_spots':available_spots,
        'occupied_spots':occupied_spots,
        'spots':spot_data
    })

@admin_dash.route('/admin/edit_lot/<int:lot_id>',methods=['GET','POST'])
@login_required
def edit_lot(lot_id):
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    lot=Parkinglot.query.get_or_404(lot_id)
    if request.method=='POST':
        lot.prime_location_name=request.form.get('name')
        lot.price_per_hour=float(request.form.get('price_per_hour'))
        lot.address=request.form.get('address')
        lot.pin_code=request.form.get('pin_code')
        new_max_spots=int(request.form.get('max_spots'))
        current_spots_count=Spot.query.filter_by(lot_id=lot.id).count()
        try:
            if(new_max_spots>current_spots_count):
                # Add new spots one by one to avoid batch insert issues
                for _ in range(new_max_spots-current_spots_count):
                    spot=Spot(lot_id=lot.id,status='A')
                    db.session.add(spot)
                    db.session.flush()  # Flush each spot individually
            elif(new_max_spots<current_spots_count):
                spots=Spot.query.filter_by(lot_id=lot.id).order_by(Spot.id.desc()).all()
                removable_spots=[s for s in spots if s.status == 'A']
                if len(removable_spots)<(current_spots_count-new_max_spots):
                    flash('Cannot reduce spots:Some spots are occupied')
                    return redirect(url_for('admin_dash.edit_lot',lot_id=lot.id))
                for i in range(current_spots_count-new_max_spots):
                    db.session.delete(removable_spots[i])
            
            lot.number_of_spots=new_max_spots
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating parking lot: {str(e)}', 'error')
            return redirect(url_for('admin_dash.edit_lot',lot_id=lot.id))
        flash('Parking lot updated Successfully!')
        return redirect(url_for('admin_dash.dash'))
    return render_template('edit_lot.html',lot=lot)

@admin_dash.route('/admin/delete_lot/<int:lot_id>',methods=['POST'])
@login_required
def delete_lot(lot_id):
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    lot=Parkinglot.query.get_or_404(lot_id)
    occupied_spots=Spot.query.filter_by(lot_id=lot.id, status='O').count()
    if occupied_spots>0:
        flash('Cannot delete parking lot: some spots are occupied.')
        return redirect(url_for('admin_dash.dash'))
    Spot.query.filter_by(lot_id=lot.id).delete()
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted Successfully!')
    return redirect(url_for('admin_dash.dash'))

@admin_dash.route('/admin/parking_summary')
@login_required
def parking_summary():
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    from sqlalchemy import func
    lots=Parkinglot.query.all()
    lot_data=[]
    earnings_data = []
    
    for lot in lots:
        total=Spot.query.filter_by(lot_id=lot.id).count()
        available=Spot.query.filter_by(lot_id=lot.id, status='A').count()
        lot_earnings = db.session.query(func.sum(Reservation.parking_cost)).join(Spot).filter(
            Spot.lot_id == lot.id,
            Reservation.leaving_timestamp.isnot(None)
        ).scalar() or 0
        lot_data.append({
            'lot':lot,
            'total_spots':total,
            'available_spots':available,
            'earnings': float(lot_earnings)
        })
        if lot_earnings > 0:
            earnings_data.append({
                'name': lot.prime_location_name,
                'earnings': float(lot_earnings)
            })    
    return render_template('parking_summary.html',lot_data=lot_data,earnings_data=earnings_data, 
                          earnings_json=json.dumps(earnings_data))

@admin_dash.route('/admin/search_spots')
@login_required
def search_spots():
    if current_user.role!='admin':
        return jsonify({'success':False,'message':'Access Denied'})
    spot_id=request.args.get('spot_id')
    lot_id=request.args.get('lot_id')
    try:
        results=[]
        if spot_id:
            spot=Spot.query.get(int(spot_id))
            if spot:
                spot_info = get_spot_details(spot)
                results.append(spot_info)
        elif lot_id:
            spots=Spot.query.filter_by(lot_id=int(lot_id)).all()
            for spot in spots:
                spot_info=get_spot_details(spot)
                results.append(spot_info)
        return jsonify({
            'success':True,
            'results':results,
            'count':len(results)
        })
    except ValueError:
        return jsonify({'success': False,'message':'Invalid spot ID or lot ID'})
    except Exception as e:
        return jsonify({'success': False,'message':'An error occurred during search'})

def get_spot_details(spot):
    """Helper function to get detailed spot information"""
    spot_info = {
        'id': spot.id,
        'status': spot.status,
        'lot_id': spot.lot_id,
        'lot_name': spot.lot.prime_location_name,
        'user_name': None,
        'vehicle_number': None,
        'parking_time': None
    }
    if spot.status == 'O':
        reservation = Reservation.query.filter_by(
            spot_id=spot.id,
            leaving_timestamp=None
        ).first()
        if reservation:
            user = User.query.get(reservation.user_id)
            spot_info['user_name'] = user.name if user else 'Unknown'
            if reservation.vehicle_id:
                vehicle = Vehicle.query.get(reservation.vehicle_id)
                spot_info['vehicle_number'] = vehicle.number if vehicle else 'N/A'
            if reservation.parking_timestamp:
                spot_info['parking_time'] = reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M')
    return spot_info

@admin_dash.route('/admin/view_users')
@login_required
def view_users():
    if current_user.role!='admin':
        flash('Access Denied')
        return redirect(url_for('user_dash.dash'))
    users=User.query.filter(User.role!='admin').all()
    return render_template('view_users.html',users=users)

@admin_dash.route('/admin/spot/<int:spot_id>/delete',methods=['POST'])
@login_required
def delete_spot(spot_id):
    if current_user.role!='admin':
        flash('Access Denied','error')
        return redirect(url_for('user_dash.dash'))
    try:
        spot=Spot.query.get_or_404(spot_id)
        lot_id=spot.lot_id
        if spot.status!='A':
            flash(f'Cannot delete Spot {spot_id} - it is currently occupied!', 'error')
            return redirect(url_for('admin_dash.view_lot_spots',lot_id=lot_id))
        pending_reservation=Reservation.query.filter_by(
            spot_id=spot_id,
            leaving_timestamp=None
        ).first()
        if pending_reservation:
            flash(f'Cannot delete Spot {spot_id} - it has an active reservation!', 'error')
            return redirect(url_for('admin_dash.view_lot_spots', lot_id=lot_id))
        db.session.delete(spot)
        db.session.commit()
        flash(f'Parking Spot {spot_id} has been successfully deleted!','success')
        return redirect(url_for('admin_dash.view_lot_spots',lot_id=lot_id))    
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the parking spot.','error')
        return redirect(url_for('admin_dash.view_lot_spots', lot_id=lot_id))