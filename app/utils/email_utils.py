from flask_mail import Message
from app import mail
from flask import current_app

def send_service_confirmation_email(user_email, subject, service_name, tracking_id, details_dict):
    msg = Message(subject, recipients=[user_email])

    body = f"""Hello,

Your {service_name} has been received.

Tracking ID: {tracking_id}
"""
    for label, value in details_dict.items():
        body += f"{label}: {value}\n"

    body += f"""

You may track the status of this request anytime via your dashboard or tracking page.

Thank you,
ServeEase Municipal Portal
"""

    msg.body = body
    mail.send(msg)

def send_service_email(recipient, subject, body, attachment=None):
    try:
        msg = Message(subject, recipients=[recipient], body=body)
    
        if attachment:
            file_data, filename = attachment
            msg.attach(filename, 'image/png', file_data.read())

        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}")
