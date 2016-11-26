import datetime


from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from . import routes

from app.app import db
from app.models import Users
from app.forms import AddUserForm


@routes.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()

    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']

    if user is None:
        redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if not form.validate():
                return render_template('adduser.html', form=form)
            else:
                newuser = Users(username=form.username.data.lower(),
                                password_hash=form.password.data,
                                role=form.role.data,
                                timestamp=datetime.datetime.now())
                db.session.add(newuser)
                db.session.commit()

                flash('User added.')
                return redirect(url_for('add_user'))

        elif request.method == 'GET':
            users = db.session.query(Users).filter(Users.role != 'admin').all()
            return render_template('adduser.html', form=form, users=users)
