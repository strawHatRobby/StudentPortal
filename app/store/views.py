from flask import render_template, redirect, url_for
from werkzeug import secure_filename
from .forms import UploadForm
from . import store
from ..models import Upload
from .. import db

@store.route('/store', methods=('GET', 'POST'))
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        upload = Upload(file_name=form.file_name.data, 
        				file_data=form.file_data.data,
        				)
        db.session.add(upload)
        
	    # flash("File uploaded successfully")
    return render_template('upload.html', form=form)

@store.route('/view')
def index():
    """List the uploads."""
    form = UploadForm()
    uploads = Upload.query.all()
    return render_template('list.html', uploads=uploads, form=form)