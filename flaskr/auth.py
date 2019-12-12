# for creating decorator to check whether the user is logged in or not
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, session, request
)

from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import get_db

# from name folder put '/auth' in front of everything related to this bp
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', method=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # getting a database connection
        db = get_db()
        error = None

        if not username:
            error = 'username not entered'
        elif not password:
            error = 'password not entered'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',
            (username,)
        ).fetchone() is not None:
            error = f'user {username} already exists!'
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', method=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        )

        if not user:
            error = 'user does not exist.'
        elif not check_password_hash(user['password'], password):
            error = 'incorrect password.'
        
        if error is None:
            # ensure no other user is logged in at the same time
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# this function runs before the view function
@bp.before_app_request
def load_logged_in_user():
    '''Session is a cookie that is passed every time a request is send.'''
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()

# when this link is visited session is cleared that is g.user gets emptied
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# this is a decorator that checks if a user is logged in or not
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('auth.login')
        return view(**kwargs)
    return wrapped_view



