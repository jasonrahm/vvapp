from app import db
from app.forms import CompetitionsForm
from app.models import Competitions
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from . import routes
import datetime


@routes.route('/competitions', methods=['GET', 'POST'])
def competitions():

    form = CompetitionsForm()

    if 'username' not in session:
        return redirect(url_for('signin'))

    user = session['username']

    if user is None:
        redirect(url_for('signin'))
    else:
        if request.method is 'POST':
            if form.validate() is False:
                return render_template('competitions.html', form=form)
            else:
                newcomp = Competitions(name=form.name.data,
                                       date=form.date.data,
                                       timestamp=datetime.datetime.now())
                db.session.add(newcomp)
                db.session.commit()

                flash('Competition successfully added.')
                return redirect(url_for('competitions'))

        elif request.method == 'GET' :
            comps = db.session.query(Competitions).all()
            return render_template('competitions.html',
                                   competitions=comps,
                                   form=form)
