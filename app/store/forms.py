from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Required
# from wtforms import ValidationEroor
# from ..models import User


class UploadForm(Form):
	file_data = FileField('Your File')
	file_name = StringField('Title')
	submit = SubmitField('Upload')
