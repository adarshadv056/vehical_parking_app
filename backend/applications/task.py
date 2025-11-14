from celery import shared_task
from datetime import timedelta, datetime, date
from models.models import *
import csv
from sqlalchemy.orm import joinedload
from applications.utils import format_report
from applications.mail import send_email
import requests
import json

@shared_task(ignore_result=False, name='download_csv_report')
def csv_report(user_id):
    parking_details = Reservation.query.options(
        joinedload(Reservation.parking_spot).joinedload(Parking_spot.parking_lot),
        joinedload(Reservation.user)
    ).filter(Reservation.user_id == user_id).all()
    csv_filename = f"user_{user_id}_parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(f'static/{csv_filename}', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Reservation ID", "Address", "Parking Lot", "Spot ID", "Vehicle No", "Start Time", "End Time", "Status","Cost"])
        for reservation in parking_details:
            status = "Parked Out" if reservation.leaving_time else "Parked"
            csv_writer.writerow([reservation.id, reservation.parking_spot.parking_lot.location,
                                 reservation.parking_spot.parking_lot.name,
                                 reservation.parking_spot.id, reservation.vehicle_number, reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
                                 reservation.leaving_time.strftime('%Y-%m-%d %H:%M') if reservation.leaving_time else 'N/A',
                                 status, reservation.parking_cost])
    return csv_filename

@shared_task(ignore_result=False, name='monthly_activity_report')
def monthly_activity_report(test_mode=True):
    today = date.today()
    users = user.query.filter_by(role='user').all()
    first_day_current_month = datetime(today.year, today.month, 1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = datetime(last_day_previous_month.year, last_day_previous_month.month, 1)
    for usr in users:
        today = datetime.today()

        user_data = {}
        user_data['username'] = usr.username
        user_data['email'] = usr.email

        parking_details = Reservation.query.options(
            joinedload(Reservation.parking_spot).joinedload(Parking_spot.parking_lot)
        ).filter(Reservation.user_id == usr.id, Reservation.parking_time >= first_day_previous_month, Reservation.parking_time < (first_day_current_month if not test_mode else today)).all()

        user_res = []

        for reservation in parking_details:
            this_res = {}
            status = "Parked Out" if reservation.leaving_time else "Parked"
            this_res['Reservation ID'] = reservation.id
            this_res['Address'] = reservation.parking_spot.parking_lot.location
            this_res['Parking Lot'] = reservation.parking_spot.parking_lot.name
            this_res['Spot ID'] = reservation.parking_spot.id
            this_res['Vehicle No'] = reservation.vehicle_number
            this_res['Status'] = status
            this_res['Start Time'] = reservation.parking_time.strftime('%Y-%m-%d %H:%M')
            this_res['End Time'] = reservation.leaving_time.strftime('%Y-%m-%d %H:%M') if reservation.leaving_time else 'N/A'
            this_res['Cost'] = reservation.parking_cost
            user_res.append(this_res)
        user_data['month_name'] = first_day_previous_month.strftime('%B')
        user_data['reservations'] = user_res
        message = format_report('static/monthly_activity_report.html', user_data)
        send_email(
            to_email=usr.email,
            subject=f'{user_data["month_name"]} Activity Report - Vehicle Parking System',
            message=message,
        )
    return 'Monthly activity report sent successfully.'

@shared_task(ignore_result=False, name='daily_reminder')
def daily_reminder():    
    today = datetime.now().date()
    new_lot_today = Parking_lot.query.filter(db.func.date(Parking_lot.created_at) == today).all()
    
    if not new_lot_today:
        return 'No new parking lot added today.'
    
    lot_names = ', '.join([lot.name for lot in new_lot_today])
    message = f"New parking lots added today: {lot_names}. Don't forget to check them out!"
    
    users = user.query.filter_by(role='user').all()
    for u in users:
        username = u.username
        headers = {'Content-Type': 'application/json'}
        payload = {
            'text': f"Hello {username}, {message}"
        }
        requests.post("https://chat.googleapis.com/v1/spaces/AAQAaMDCL-c/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=gSCq7RLZA1ulbWRwX8mYziTLYCTmbZGw7-FjRNxk3yQ", data=json.dumps(payload), headers=headers)
    return 'Daily reminder sent successfully.'