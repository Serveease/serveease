from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Feedback
import os
import random
from app.utils.email_utils import send_service_email

feedback = Blueprint('feedback', __name__)

@feedback.route('/submit-feedback', methods=['GET', 'POST'])
@login_required
def submit_feedback():
    if request.method == 'POST':
        message = request.form.get('message')
        tracking_number = "FDB" + str(random.randint(100000, 999999))

        fb = Feedback(
            user_id=current_user.id,
            message=message,
            tracking_number=tracking_number
        )
        db.session.add(fb)
        db.session.commit()

        send_service_email(
            recipient=current_user.email,
            subject="📝 Feedback Submitted",
            body=f"""Hello {current_user.name},

        Thank you for your feedback!

        📌 Tracking Number: {tracking_number}
        💬 Message: {fb.message}
        📅 Date: {fb.date_created.strftime('%Y-%m-%d')}

        We appreciate your input.

        Regards,
        ServeEase Team
        """
        )


        flash('Feedback submitted!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('submit_feedback.html')

@feedback.route('/view-feedback')
@login_required
def view_feedback():
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(Feedback.id.desc()).all()
    return render_template('view_feedback.html', feedbacks=feedbacks)
