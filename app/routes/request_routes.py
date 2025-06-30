import os, random
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import DocumentRequest
from app.utils.email_utils import send_service_confirmation_email
from app.utils.email_utils import send_service_email

request_bp = Blueprint('requests', __name__)
UPLOAD_FOLDER = 'app/static/uploads/'

@request_bp.route('/request-document', methods=['GET', 'POST'])
@login_required
def request_document():
    if request.method == 'POST':
        document_type = request.form['document_type']
        purpose = request.form['purpose']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
        else:
            filename = None

        tracking_number = "REQ" + str(random.randint(100000, 999999))
        new_request = DocumentRequest(
            user_id=current_user.id,
            document_type=document_type,
            purpose=purpose,
            filename=filename,
            tracking_number=tracking_number
        )
        db.session.add(new_request)
        db.session.commit()

        send_service_email(
            recipient=current_user.email,
            subject="📄 Document Request Submitted",
            body=f"""Hello {current_user.name},

        You have submitted a document request.

        📌 Tracking Number: {tracking_number}
        📄 Document Type: {document_type}
        🎯 Purpose: {purpose}
        📅 Date: {new_request.created_at.strftime('%Y-%m-%d')}

        You can track this at: https://serveease-t64f.onrender.com

        Regards,
        ServeEase Team
        """
        )

        flash("Your request has been submitted. A confirmation email has been sent.", "success")
        return redirect(url_for('requests.track_requests'))

    return render_template('request_document.html')


@request_bp.route('/track-requests')
@login_required
def track_requests():
    requests_list = DocumentRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('track_results/unified_result.html', requests=requests_list)
