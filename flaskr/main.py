import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/cources', methods=('GET', 'POST'))
def cources():
    # LameOver

    pass

@bp.route('/', methods=('GET'))
def main():
    # SuperCreator2007

    pass

@bp.route('/profile/<id>', methods=('GET'))
def profile(id):
    # Zircle XeroxPy

    pass

@bp.route('/cources/<id>', methods=('GET'))
def cource_description(id):
    # hochi...
    pass

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
