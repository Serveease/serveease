from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Appointment

appointment = Blueprint('appointment', __name__)

@appointment.route('/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        purpose = request.form.get('purpose')
        date = request.form.get('schedule_date')

        new_appt = Appointment(
            user_id=current_user.id,
            purpose=purpose,
            schedule_date=date
        )
        db.session.add(new_appt)
        db.session.commit()

        flash('Appointment booked!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('book_appointment.html')

@appointment.route('/view-appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('view_appointments.html', appointments=appointments)