from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import DownloadableForm
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import DocumentRequest, Appointment, Payment, Feedback

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', user=current_user)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_as_user_dashboard.html', user=current_user)
    return render_template('dashboard.html', user=current_user)

@main.route('/forms')
@login_required
def view_forms():
    forms = DownloadableForm.query.order_by(DownloadableForm.uploaded_at.desc()).all()
    return render_template('forms.html', forms=forms)

@main.route('/history')
@login_required
def service_history():
    doc_requests = DocumentRequest.query.filter_by(user_id=current_user.id).all()
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).all()

    return render_template('user/service_history.html',
                           doc_requests=doc_requests,
                           appointments=appointments,
                           payments=payments,
                           feedbacks=feedbacks)

