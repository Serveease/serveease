from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import DocumentRequest
from app import db
from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    all_requests = DocumentRequest.query.all()
    return render_template('admin_dashboard.html', requests=all_requests)

@admin.route('/admin/update-status/<int:request_id>', methods=['POST'])
@login_required
def update_status(request_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    new_status = request.form.get('status')
    req = DocumentRequest.query.get_or_404(request_id)
    req.status = new_status
    db.session.commit()
    flash('Status updated.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
