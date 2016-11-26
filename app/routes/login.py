from app.forms import LoginForm
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from . import routes


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            session['username'] = form.username.data
            flash('Login Successful.')
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)
