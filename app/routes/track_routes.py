from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import DocumentRequest, Appointment, Payment, Feedback

track_bp = Blueprint('track', __name__)

@track_bp.route('/track-services', methods=['GET', 'POST'])
@login_required
def track_services():
    return render_template('user/track_services.html')

@track_bp.route('/track-request', methods=['POST'])
@login_required
def track_request():
    tracking_number = request.form.get('tracking_number')

    doc = DocumentRequest.query.filter_by(tracking_number=tracking_number).first()
    app = Appointment.query.filter_by(tracking_number=tracking_number).first()
    pay = Payment.query.filter_by(tracking_number=tracking_number).first()
    fb = Feedback.query.filter_by(tracking_number=tracking_number).first()

    return render_template('track_results/unified_result.html',
                       doc=doc,
                       app=app,
                       pay=pay,
                       fb=fb)

