from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Payment
import uuid

payment = Blueprint('payment', __name__)

@payment.route('/make-payment', methods=['GET', 'POST'])
@login_required
def make_payment():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        purpose = request.form.get('purpose')
        txn_id = str(uuid.uuid4())[:8]

        new_payment = Payment(
            user_id=current_user.id,
            amount=amount,
            purpose=purpose,
            transaction_id=txn_id,
            status="Completed"
        )
        db.session.add(new_payment)
        db.session.commit()

        flash(f'Payment successful. Transaction ID: {txn_id}', 'success')
        return redirect(url_for('payment.payment_history'))

    return render_template('make_payment.html')

@payment.route('/payment-history')
@login_required
def payment_history():
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    return render_template('payment_history.html', payments=payments)