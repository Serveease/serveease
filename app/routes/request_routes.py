from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import DocumentRequest

request_bp = Blueprint('requests', __name__)

@request_bp.route('/request-document', methods=['GET', 'POST'])
@login_required
def request_document():
    if request.method == 'POST':
        doc_type = request.form.get('doc_type')
        purpose = request.form.get('purpose')

        new_request = DocumentRequest(
            user_id=current_user.id,
            document_type=doc_type,
            purpose=purpose,
            status="Received"
        )
        db.session.add(new_request)
        db.session.commit()

        flash("Document request submitted!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('request_document.html')

@request_bp.route('/track-requests')
@login_required
def track_requests():
    user_requests = DocumentRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('track_requests.html', requests=user_requests)