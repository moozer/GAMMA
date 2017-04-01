from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from datetime import date, datetime
from datastore import *

app = Flask(__name__)
ds = Datastore( filename="data/gamma.db")

# might need improving...
def login_user( user, passwd ):
    return user

def get_points_per_user( userid ):
    return {'absence': 1, 'attendance': 10, 'handins': 6, 'extra': 5, 'sum': 20 }

@app.route('/')
def index():
    return render_template('index.html')

## --------- admin pages -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        userid = login_user( request.form['username'], request.form['password'] )
        if not userid:
            error = 'Permission denied, credentials rejected'
        else:
            session['userid'] = userid
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

## --------- points pages -----------------
@app.route('/points')
@app.route('/points/<studentid>')
def points( studentid=None ):
    if not studentid:
        students = ds.get_student_ids()
        points_list = []
        for s in students:
            points_list.append( { "id": s, "name": ds.get_student(s).name,
                                "points": get_points_per_user(s) } )

        return render_template('points_overview.html', points_list=points_list)
    else:
        name = ds.get_student(studentid).name
        lesson_points_list = ds.get_lesson_points_by_stud( studentid )
        extra_points_list = ds.get_extra_points_by_student( studentid )

        return render_template('points_student.html',
                               studname=name,
                               lesson_points_list=lesson_points_list,
                               extra_points_list=extra_points_list
                               )

## --------- points pages -----------------
# TODO: we want this:
#       https://stackoverflow.com/questions/31669864/date-in-flask-url
@app.route('/lessons')
@app.route('/lessons/<lesson_date_str>')
def lessons( lesson_date_str=None ):
    if not lesson_date_str:
        lessons = ds.get_lessons_list()
        return render_template('lessons_overview.html', lessons = lessons)
    else:
        lesson_date = datetime.strptime(lesson_date_str, "%Y-%m-%d").date()
        s = ds.get_lesson( lesson_date )
        sp = ds.get_lesson_points_by_lesson( lesson_date )
        return render_template('lessons_detailed.html', lesson=s, points=sp )


if __name__ == "__main__":
    app.secret_key = 'super secret key'

    # init_db( ds )
    app.run()
