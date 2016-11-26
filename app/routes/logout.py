from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from . import routes


@routes.route('/signout')
def signout():

    if 'username' not in session:
        redirect(url_for('login'))

    session.pop('username', None)

    flash('You have been logged out.')
    return redirect(url_for('index'))