from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Announcement
from app import db

announcement = Blueprint('announcement', __name__)

@announcement.route('/announcements')
def view_announcements():
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    return render_template('announcements.html', announcements=announcements)

@announcement.route('/admin/post-announcement', methods=['GET', 'POST'])
@login_required
def post_announcement():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_announcement = Announcement(title=title, content=content)
        db.session.add(new_announcement)
        db.session.commit()

        flash('Announcement posted.', 'success')
        return redirect(url_for('announcement.view_announcements'))

    return render_template('admin_dashboard.html') 