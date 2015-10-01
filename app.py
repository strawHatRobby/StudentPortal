from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'will add later'
# engine = create_engine('mysql+mysqldb://root:@localhost/')
# manager.add_command('app', app.run())

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


# comments = [
# 	"This is just ranom words",
# 	"lets hope this will work",
# 	"yeah",
# ]


class Teacher(db.Model):
	__tablename__ = "Teacher"
	teacher_id = db.Column(db.Integer, primary_key=True)
	teacher_name = db.Column(db.String(64), unique=True)
	# user = ForeignKeyField(
	# 	rel_model=User,
	# 	related_name='posts'
	# 	)
	student_of = db.relationship('Student', backref='taught_by')
	# student_of = db.relationship('Student', backref='taught_by', lazy=dynamic)
	# with the lazy=dynamic queries are not automatically executed

	def __repr__(self):
		return '<Teacher %r>' % self.teacher_name


class Student(db.Model):
	__tablename__ = "Student"
	studnet_id = db.Column(db.Integer, primary_key=True)
	student_name = db.Column(db.String(64), unique=True)
	taught_id = db.Column(db.Integer, db.ForeignKey('Teacher.teacher_id'))

	def __repr__(self):
		return '<Student> %r' % self.student_name


def make_shell_context():
	return dict(app=app, db=db, Teacher=Teacher, Student=Student)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


class NameForm(Form):
	name = StringField('Enter your name?', validators=[Required()])
	upload = FileField('Click to upload your file')
	submit = SubmitField('Submit')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/<name>/', methods=['GET', 'POST'])
def user(name):
	form = NameForm()
	upload = None
	if form.validate_on_submit():
		old_name = session.get['name']
		if old_name is not None and old_name != form.name.data:
			flash("Boy you're using your old name")

		session[name] = form.name.data
		form.name.data = ''
		upload = form.upload.data
		return redirect(url_for('index'))
	return render_template(
		'user.html',
		form=form,
		name=session.get('name'),
		upload=upload)


if __name__ == "__main__":
	manager.run()
