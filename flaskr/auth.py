# CleverCat07 &Matsenko
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['nick']
        password = request.form['password']
        name = request.form['first_name']
        email = request.form['email']
        prof_skills = request.form['skills']
        birthday = request.form['age']
        telephone_number=request.form['phone']
        db = get_db()
        error = None
        if db.execute(
            'SELECT id FROM user_tab WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            return "Користувач з таким ніком вже зареєстрованний"

        if error is None:
            db.execute(
                'INSERT INTO user_tab (username, password,name,email,telephone_number,   prof_skills   ,birthday) VALUES (?, ?,?,?,?,?,?)',
                (username, generate_password_hash(password),name,email,telephone_number,prof_skills,birthday)
            )
            db.commit()
            return "Ви зареєструвалися!"

        flash(error)

    return "Все ок"



##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['nick']
        password = request.form['password']
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
            return "Все ок"

        flash(error)

    return render_template('log_vol.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user_tab WHERE id = ?', (user_id,)
        ).fetchone()    
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@bp.route('/create_course', methods=('GET', 'POST'))
def course():
    if request.method == 'POST':
        course_name = request.form['name']
        descr = request.form['descr']
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not descr:
            error = 'Please enter description'
        elif db.execute(
            'SELECT * FROM course WHERE name = ?', (name,)
        ).fetchone() is not None:
            error = 'Name of course {} is already registered.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO user (name, password) VALUES (?, ?)',
                (name, descr)
            )
            db.commit()
            return redirect(url_for('auth.create_course'))

        flash(error)

    return render_template('create_course.html')
@bp.route('/course_list', methods=('GET', 'POST'))
def list():
	return render_template(url_for('auth.course_list'))