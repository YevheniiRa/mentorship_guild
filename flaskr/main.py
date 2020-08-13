import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from . import auth
bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/course/create', methods=('GET', 'POST'))
def course_create():
    if request.method == 'POST':
        username = g.user['username']
        password = g.user['password']
        course_start = request.form['course_start']
        about_course = request.form['course_description']
        course_name= request.form['course_name']
        volunteers=request.form['volunteers']
        min_age=request.form['min_age']
        max_age=request.form['max_age']
        end_date=request.form['course_end']
        min_people=request.form['min_people']
        max_people=request.form['max_people']
        schedule=request.form['schedule']
        min_knowledge=request.form['min_knowledge']
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
                (g.user['id'],course_name,course_start,about_course,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge )
            )
            db.commit()
            return  redirect(url_for('main.course_list'))
        flash(error)
    if request.method == 'GET':
        return render_template("course_create.html")

            

        

    
@bp.route('/course/list')
def course_list():
    db = get_db()
    courses = db.execute(
        'SELECT id,name, start_date, descr, students_id, author_id,volunteers,min_age,max_age,end_date,min_people,max_people,schedule,min_knowledge'
        ' FROM course '
        
    ).fetchall()
    mentor = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()
    student = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()

    return render_template('course_list.html',courses=courses,mentor=mentor,student=student)  
    
@bp.route('course/<int:course_id>/list', methods=('POST', ))
@auth.login_required
def course_delete(course_id):
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM course WHERE id = ?', (course_id,))
        db.commit()
        return redirect(url_for('main.course_list'))



    
@bp.route('/course/<int:course_id>/list/connect/<int:student_id>', methods=('POST',)) 
@auth.login_required
def course_connect(course_id,student_id): 
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO course (students_id) WHERE id = ?' ' VALUES (?)',(student_id))
        db.commit()
        return redirect(url_for('main.course_list'))
   


        
    

