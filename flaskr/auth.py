# CleverCat07 &Matsenko
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/')
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
        isMentor=request.form['mentor']
        db = get_db()
        error = None
        if db.execute(
            'SELECT id FROM user_tab WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            return render_template("reg.html")
        if db.execute(
    'SELECT id FROM user_tab WHERE email = ?', (email,)
        ).fetchone() is not None:
            return "Користувач з такою поштую вже зареєстрованний"    

        if error is None:
            db.execute(
                'INSERT INTO user_tab (username, password,name,email,telephone_number,   prof_skills   ,birthday,isMentor) VALUES (?, ?,?,?,?,?,?,?)',
                (username, generate_password_hash(password),name,email,telephone_number,prof_skills,birthday,isMentor)
            )
            db.commit()
            return  redirect(url_for('auth.login'))

        flash(error)
    if request.method == 'GET':
        return render_template('reg.html')


    
    



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
            return  redirect(url_for('home'))

        flash(error)
    if request.method == 'GET':
        return render_template('log.html')


    


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
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view     
