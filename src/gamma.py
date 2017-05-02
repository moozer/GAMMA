from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

from datetime import date, datetime
from datastore import *

# Charts
import pygal
from pygal.style import BlueStyle

# Forms
from admin import forms


app = Flask(__name__)
ds = Datastore()

# might need improving...
test_user = 'john0000'
test_password = 'gamma'
def check_credentials( user, passwd ):
	if user == test_user and passwd == test_password:
		return True

@app.route('/')
def index():
	title = 'Home'
	return render_template("index.html",
							title = title
							)

## --------- admin pages -----------------
@app.route('/login/', methods=['GET', 'POST'])
def login():
	title = 'Login'
	form = forms.LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			registered_user = check_credentials( form.username.data, form.password.data )
			if not registered_user:
				flash('Permission denied, credentials rejected', 'error')
			else:
				session['userid'] = form.username.data
				session['logged_in'] = True
				flash('You were logged in', 'success')
				return redirect(url_for('index'))
		else:
			flash('Please fill in required fields.', 'error')

	return render_template('page_login.html',
							title = title,
							form = form,
							test_user = test_user,
							test_password = test_password
							)


@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out', 'success')
	return redirect(url_for('index'))

## --------- points pages -----------------
@app.route('/points/')
@app.route('/points/<studentid>')
def points( studentid=None ):
	title = 'Student Points'
	if studentid and ds.check_user(studentid):
		name = ds.get_student(studentid).name
		lesson_points_list = ds.get_lesson_points_by_stud( studentid )
		extra_points_list = ds.get_extra_points_by_student( studentid )
		lessons = []
		for l in lesson_points_list:
			lessons.append({ 'lessons': ds.get_lesson(l.lesson_id) })
			# more is needed - hand-ins and absence lists

		return render_template('page_points_student.html',
								studname=name,
								lessons=lessons,
								extra_points_list=extra_points_list,
								title = title
								)
	else:
		# Show error if a wrong user is supplied
		if studentid and not ds.check_user(studentid):
			flash('User not found', 'error')

		students = ds.get_student_ids()
		points_list = []
		for s in students:
			points_list.append( { "id": s, "name": ds.get_student(s).name,
								"points": ds.get_sum_by_student(s),
								'sum': ds.get_sum_by_student(s).attendance +
										ds.get_sum_by_student(s).handins +
										ds.get_sum_by_student(s).extra -
										ds.get_sum_by_student(s).absence} )
		# Build Chart
		graph = pygal.Bar(style=BlueStyle)
		graph.title = 'Student Points'
		graph.x_labels = [student['name'] for student in points_list]
		graph.add('Attendance',
					[student['points'][0] for student in points_list])
		graph.add('Handins',
					[student['points'][1] for student in points_list])
		graph.add('Absence',
					[student['points'][2] for student in points_list])
		graph.add('Extra Points',
					[student['points'][3] for student in points_list])
		graph.add('Total Points',
					[student['sum'] for student in points_list])
		graph_data = graph.render_data_uri()

		return render_template('page_points_overview.html',
								graph_data = graph_data,
								points_list = points_list,
								title = title
								)

## --------- points pages -----------------
# TODO: we want this:
#	https://stackoverflow.com/questions/31669864/date-in-flask-url
@app.route('/lessons/')
@app.route('/lessons/<lesson_date_str>')
def lessons( lesson_date_str=None ):
	title = 'Lessons'
	if not lesson_date_str:
		lessons = ds.get_lessons_list()
		return render_template('page_lessons_overview.html',
								lessons = lessons,
								title = title
								)
	else:
		lesson_date = datetime.strptime(lesson_date_str, "%Y-%m-%d").date()
		s = ds.get_lesson_by_date( lesson_date )
		sp = ds.get_lesson_points_by_lesson( lesson_date )
		title = 'Lesson ' + s.name +' Details'
		return render_template('page_lessons_detailed.html',
								lesson=s,
								points=sp,
								title = title
								)

@app.errorhandler(404)
def page_not_found(e):
	title = 'Page Not Found'
	return render_template('page_404.html',
							title = title
							), 404

def init_db( ds ):
	student_count = 10
	lessons_count = 12
	extra_points_count = 3

	for i in range( 0,student_count ):
		ds.add_student( student_record( 'john%04d'%(i, ), "John %d"%(i,) ) )

	for i in range( 0,lessons_count ):
		ds.add_lesson( lesson_record( 'LearningSession%04d'%(i, ), date( 2017, 02, i+1) ) )

	for user_i in range( 0,student_count ):
		for lesson_i in range( 0,lessons_count ):
			ds.add_lesson_points(
				lesson_points_record( date( 2017, 02, lesson_i+1), 'john%04d'%(user_i, ),
										True, False, True ) )

	for user_i in range( student_count ):
		for ep_i in range( extra_points_count ):
			ds.add_extra_points(
					extra_points_record(
						date( 2017, 02, ep_i+1),
						student_id='john%04d'%(user_i, ),
						points=1,
						reason="Some valid reason #%d" % (user_i+ep_i, )
						))


if __name__ == "__main__":
	app.secret_key = 'super secret key'

	init_db( ds )
	app.run(debug=False)
