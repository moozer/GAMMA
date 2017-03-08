from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from datastore.datastore import Datastore
from datastore.student import student_record
from datastore.session import session_record

from datetime import date, datetime

app = Flask(__name__)
ds = Datastore()

# might need improving...
def login_user( user, passwd ):
    return user

def get_points_per_user( userid ):
    return {'absence': 1, 'attendance': 10, 'handins': 6, 'extra': 5, 'sum': 20 }

def get_points_list_per_user( userid ):
    absence =   [   { "date": "20170302", "session": "ITT1 SD" }]
    attendance = [  { "date": "20170302", "session": "ITT1 SD", "sessionid": 23 },
                    { "date": "20170102", "session": "ITT1 SD", "sessionid": 24 },
                    { "date": "20170109", "session": "ITT1 SD", "sessionid": 25 },
                    { "date": "20170116", "session": "ITT1 SD", "sessionid": 26 },
                    { "date": "20170123", "session": "ITT1 SD", "sessionid": 27 },
                    { "date": "20170130", "session": "ITT1 SD", "sessionid": 28 },
                    { "date": "20170207", "session": "ITT1 SD", "sessionid": 29 },
                    { "date": "20170214", "session": "ITT1 SD", "sessionid": 20 },
                    { "date": "20170221", "session": "ITT1 SD", "sessionid": 21 } ]
    handins = [     { "date": "20170302", "session": "ITT1 SD", "sessionid": 23 },
                    { "date": "20170102", "session": "ITT1 SD", "sessionid": 24 },
                    { "date": "20170109", "session": "ITT1 SD", "sessionid": 25 },
                    { "date": "20170116", "session": "ITT1 SD", "sessionid": 26 },
                    { "date": "20170123", "session": "ITT1 SD", "sessionid": 27 },
                    { "date": "20170130", "session": "ITT1 SD", "sessionid": 28 } ]
    extra = [       { "date": "20170202",
                        "reason": "Awarded by class because of awesomeness", "points": 2},
                    { "date": "20170202",
                        "reason": "Participated in some event", "points": 1},
                    { "date": "20170202",
                        "reason": "Did something else that was awesome", "points": 2}  ]
    return { 'absence': absence, "attendance": attendance,
            "handins": handins, "extra": extra}


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
        points_list = get_points_list_per_user( studentid )

        return render_template('points_student.html', studname=name, points_list=points_list)

## --------- points pages -----------------
# TODO: we want this:
#       https://stackoverflow.com/questions/31669864/date-in-flask-url
@app.route('/sessions')
@app.route('/sessions/<session_date>')
def sessions( session_date=None ):
    if not session_date:
        sessions = ds.get_sessions_list()
        return render_template('sessions_overview.html', sessions = sessions)
    else:
        s = ds.get_session( datetime.strptime(session_date, "%Y-%m-%d").date() )
        return render_template('sessions_detailed.html', session=s )

def init_db( ds ):
    for i in range( 0,10 ):
        ds.add_student( student_record( 'john%04d'%(i, ), "John %d"%(i,) ) )

    for i in range( 0,10 ):
        ds.add_session( session_record( 'LearningSession%04d'%(i, ), date( 2017, 02, i+1) ) )

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    init_db( ds )
    app.run()
