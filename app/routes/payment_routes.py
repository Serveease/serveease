from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Payment
import uuid
import os
import random
import qrcode
from io import BytesIO
from flask import send_file
from app.utils.email_utils import send_service_email
from datetime import datetime


payment = Blueprint('payment', __name__)

@payment.route('/make-payment', methods=['GET', 'POST'])
@login_required
def make_payment():
    if request.method == 'POST':
        amount = request.form.get('amount')
        method = request.form.get('method')
        tracking_number = "PAY" + str(random.randint(100000, 999999))

        new_payment = Payment(
            user_id=current_user.id,
            amount=amount,
            method=method,
            tracking_number=tracking_number,
            date=datetime.now()
        )
        db.session.add(new_payment)
        db.session.commit()

        qr_data = f"Tracking Number: {tracking_number}\nAmount: ₱{amount}\nMethod: {method}"
        qr_img = qrcode.make(qr_data)
        qr_io = BytesIO()
        qr_img.save(qr_io, 'PNG')
        qr_io.seek(0)

        send_service_email(
            recipient=current_user.email,
            subject="💳 Payment Received",
            body=f"""Hello {current_user.name},

            Your payment has been successfully processed.

            📌 Tracking Number: {tracking_number}
            💵 Amount: ₱{amount}
            💳 Method: {method}
            📅 Date: {new_payment.date.strftime('%Y-%m-%d')}

            Track your payment at: https://serveease-t64f.onrender.com

            Regards,  
            ServeEase Team
            """,
            attachment=(qr_io, 'qr.png')
        )

        flash('Payment successful!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('make_payment.html')


@payment.route('/payment-history')
@login_required
def payment_history():
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    return render_template('payment_history.html', payments=payments)