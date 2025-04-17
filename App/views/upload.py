from flask import Blueprint, send_from_directory
import os
upload_views = Blueprint('upload_views', __name__)

@upload_views.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)