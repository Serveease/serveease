from flask import Blueprint, render_template, send_from_directory
import os

file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/downloadable-forms')
def downloadable_forms():
    files = os.listdir('app/static/downloads')
    return render_template('downloadable_forms.html', files=files)

@file_routes.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('app/static/downloads', filename, as_attachment=True)