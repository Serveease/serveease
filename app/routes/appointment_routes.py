from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Appointment
import os
import random
from datetime import datetime
from app.utils.email_utils import send_service_email

appointment = Blueprint('appointment', __name__)

@appointment.route('/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        purpose = request.form.get('purpose')
        date_str = request.form.get('schedule_date')

        # ✅ Convert string to datetime object
        schedule_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        tracking_number = "APT" + str(random.randint(100000, 999999))
        new_appt = Appointment(
            user_id=current_user.id,
            purpose=purpose,
            schedule_date=schedule_date,  # <-- Store as datetime
            tracking_number=tracking_number
        )
        db.session.add(new_appt)
        db.session.commit()

        send_service_email(
            recipient=current_user.email,
            subject="📅 Appointment Scheduled",
            body=f"""Hello {current_user.name},

Your appointment has been successfully scheduled.

📌 Tracking Number: {tracking_number}
🗓️ Schedule: {schedule_date.strftime('%Y-%m-%d %H:%M')}
💼 Purpose: {purpose}
📅 Date Created: {new_appt.created_at.strftime('%Y-%m-%d')}

Track your appointment at: https://serveease-t64f.onrender.com

Regards,
ServeEase Team
"""
        )

        flash('Appointment booked!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('book_appointment.html')


@appointment.route('/view-appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('view_appointments.html', appointments=appointments)
