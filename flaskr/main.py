import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from . import auth
import requests
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/course/create', methods=('GET', 'POST'))
def course_create():
    if request.method == 'POST':
        username = g.user['username']
        password = g.user['password']
        course_start = request.form['course_start']
        about_course = request.form['course_description']
        course_name = request.form['course_name']
        volunteers = request.form['volunteers']
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        end_date = request.form['course_end']
        min_people = request.form['min_people']
        max_people = request.form['max_people']
        schedule = request.form['schedule']
        min_knowledge = request.form['min_knowledge']
        db = get_db()
        error = None
        g.user = db.execute(
            'SELECT * FROM user_tab WHERE username = ?', (username,)
        ).fetchone()

        if error is None:
            session.clear()
            session['user_id'] = g.user['id']
            db.execute(
                'INSERT INTO course (author_id,name,start_date,descr,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge  ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                (g.user['id'], course_name, course_start, about_course, volunteers, min_age,
                 max_age, end_date, min_people, max_people, schedule, min_knowledge)
            )
            db.commit()
            return redirect(url_for('main.course_list'))
        flash(error)
    if request.method == 'GET':
        return render_template("course_create.html")


@bp.route('/course/list')
def course_list():
    db = get_db()
    courses = db.execute(
        'SELECT id,name, start_date, descr,  author_id,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge'
        ' FROM course '

    ).fetchall()
    mentor = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()
    student = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()
    student_in_course = db.execute('SELECT course_id,student_id ' 'FROM  students_in_course').fetchall()
    # send_simple_message()
    return render_template('course_list.html', courses=courses, mentor=mentor, student=student,student_in_course=student_in_course)


@bp.route('course/<int:course_id>/delete', methods=("POST",))
@auth.login_required
def course_delete(course_id):
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM course WHERE id = ?', (course_id,))
        db.commit()
        return redirect(url_for('main.course_list'))


@bp.route('/course/<int:course_id>/list/connect/<int:student_id>', methods=("GET",))
@auth.login_required
def course_connect(course_id, student_id):
    if request.method == 'GET':
        db = get_db()


        db.execute(
            'INSERT INTO students_in_course (course_id, student_id) VALUES (?, ?)',
            (course_id, student_id)
        )                   
        db.commit()
        return redirect(url_for('main.course_list'))


@bp.route('/profile')
def profile():
    return render_template("profile.html")


@bp.route('course/edit/<int:course_id>', methods=("GET",))
def course_edit_(course_id):
    if request.method == 'GET':
        db = get_db()
        courses = db.execute(
        'SELECT id,name, start_date, descr,  author_id,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge'
        ' FROM course '

        ).fetchall()
        return render_template("course_edit.html",course_id=course_id,courses=courses)




@bp.route('/profile/change/data', methods=('GET', 'POST'))
def profile_change_data():
    if request.method == 'POST':
        username = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        prof_skills = request.form["prof_skills"]
        birthday = request.form["birthday"]
        telephone_number = request.form["telephone_number"]
        db = get_db()
        error = None
        if username == g.user['username']:
            if error is None:

                db.execute("UPDATE user_tab SET username=?,name=?,email=?,telephone_number=?,birthday=?,prof_skills=? WHERE id=?",
                           (username, name, email, prof_skills, birthday, telephone_number, g.user['id'],))
                db.commit()
                return redirect(url_for('home'))

        else:
            if db.execute(
                'SELECT id FROM user_tab WHERE username = ?', (username,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                return "Користувач з таким ніком вже зареєстрованний"

        flash(error)

    if request.method == 'GET':

        return render_template("profile_change_data.html")


@bp.route('/course/<int:course_id>/edit',methods=("POST",))
def course_edit(course_id):
    if request.method == 'POST':
        course_start = request.form['course_start']
        about_course = request.form['course_descr']
        course_name = request.form['course_name']
        volunteers = request.form['volunteers']
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        end_date = request.form['course_end']
        min_people = request.form['min_students']
        max_people = request.form['max_students']
        schedule = request.form['schedule']
        min_knowledge = request.form['min_skills']
        db = get_db()
        error = None
        if error is None:
            session.clear()
            session['user_id'] = g.user['id']
            db.execute("UPDATE course SET name=?,start_date=?,descr=?,volunteers=?,min_age=?,max_age=?,end_date=?,min_people=?,max_people=?,schedule=?,min_knowledge=? WHERE id=?",
                      (course_name,course_start , about_course,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge,course_id))
            db.commit()
            return redirect(url_for('main.course_list'))
        flash(error)




# @bp.route('/course/<int:course_id>/list/leave/<int:student_id>', methods=("GET",))
# @auth.login_required
# def course_leave(course_id,student_id):
#     if request.method == 'GET':
#         db = get_db()
#         db.execute("UPDATE course SET students_id=? WHERE id=?",
#                    (student_id, course_id,))
#         db.commit()
#         return redirect(url_for('main.course_list'))


# @bp.route('/course/edit/<int:course_id>')
# def course_edit(course_id):
#     return render_template("course_edit.html")

# @bp.route('/course/<int:course_id>/edit', methods=("GET",))
# def course_id_edit(course_id):
#     if request.method == 'GET':
#         return redirect(url_for('main.course_edit',course_id=course_id))  







def send_mail():
    pass











# def send_simple_message():
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandboxe45998f6366f4717b092f21ae2b1cc30.mailgun.org",
# 		auth=("api", "a01ed38829e1288df0006b8d9d3ee04d-203ef6d0-3a5707f2"),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["vmatcenko@ukr.net", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomness!"})
