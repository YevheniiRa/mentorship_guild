import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/')
@bp.route('/course/create', methods=('GET', 'POST'))
def courses_create():
    if request.method == 'POST':
        username = request.form['nick']
        password = request.form['password']
        course_date = request.form['course_date']
        about_course = request.form['about_course']
        course_name= request.form['name']
        db = get_db() 
        error = None
        user = db.execute(
            'SELECT * FROM user_tab WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
            return "Неправильний пароль або нік. "
            
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            return "Неправильний пароль або нік. "

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            db.execute(
                'INSERT INTO course (start_date, name,author_id,descr   ) VALUES (?,?,?,?)',
                (course_date, course_name,user['id'],about_course )
            )
            db.commit()
            return "Ви створили курс!" 
        flash(error)
    if request.method == 'GET':
        return render_template("course_create.html")

            

        

    
@bp.route('/course/list')
def course_list():
    db = get_db()
    courses = db.execute(
        'SELECT name, start_date, descr, students_id, author_id'
        ' FROM course '
        
    ).fetchall()
    mentor = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()
    student = db.execute('SELECT username,id ' 'FROM user_tab').fetchall()

    return render_template('course_list.html',courses=courses,mentor=mentor,student=student)  

    
   
        
    



# @bp.route('/', methods=('GET'))
# def main():
#     # SuperCreator2007

#     pass

# @bp.route('/profile/<id>', methods=('GET'))
# def profile(id):
#     # Zircle XeroxPy

#     pass

# @bp.route('/courses/<id>', methods=('GET'))
# def cource_description(id):
#     # hochi...
#     pass

# @bp.route('/orders/', methods=('GET', 'POST'))
# def orders():
#     # 

#     pass

# @bp.route('/orders/<id>', methods=('GET'))
# def orders(id):
#     # 

#     pass

# @bp.route('/orders/<id>', methods=('GET'))
# def orders(id):
#     # 

#     pass
