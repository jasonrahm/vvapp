from app import app
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from forms import CompetitionsForm
from forms import CompetitionTeamForm
from forms import LoginForm
from forms import TeamForm
from models import db
from models import Competitions
from models import CompetitionTeam
from models import Teams

import datetime


@app.errorhandler(404)
def missing_file(error):
    return render_template('servererror.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/competitions', methods=['GET', 'POST'])
def competitions():

    form = CompetitionsForm()

    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']

    if user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if not form.validate():
                return render_template('competitions.html', form=form)
            else:
                newcomp = Competitions(name=form.name.data,
                                       date=form.date.data,
                                       timestamp=datetime.datetime.now())
                db.session.add(newcomp)
                db.session.commit()

                flash('Competition successfully added.')
                return redirect(url_for('competitions'))

        elif request.method == 'GET':
            comps = db.session.query(Competitions).all()
            return render_template('competitions.html',
                                   competitions=comps,
                                   form=form)


@app.route('/competitions/<int:id>', methods=['GET', 'POST'])
def manage_competition(id):

    form = CompetitionTeamForm(request.values, competition=id)
    comp = Competitions.query.get(id)
    form.competition = comp.name
    form.team.choices = [(a.id, a.number) for a in Teams.query.all()]

    user = session['username']

    teams = db.session.query(CompetitionTeam).filter(
        CompetitionTeam.competitions == id).all()
    team_list = []
    for team in teams:
        team_list.append(int(team.teams))
    team_data = db.session.query(Teams).filter(
        Teams.id.in_(team_list)).order_by(Teams.number).all()

    if user is None:
        redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if not form.validate():
                return render_template('competition_details.html',
                                       form=form,
                                       id=id,
                                       team_data=team_data)
            else:
                postdata = request.values
                comp = int(postdata['competition'])
                team = int(postdata['team'])

                newteam = CompetitionTeam(competitions=comp,
                                          teams=team,
                                          timestamp=datetime.datetime.now())
                db.session.add(newteam)
                db.session.commit()

                flash('Team successfully added to the competition.')
                return redirect(url_for('manage_competition', id=id))

        elif request.method == 'GET':
            return render_template('competition_details.html',
                                   form=form,
                                   id=id,
                                   team_data=team_data)


@app.route('/competitions/delete/<int:id>', methods=['GET'])
def delete_competition_entry(id):

    user = session['username']
    if user is None:
        return redirect(url_for('login'))
    else:
        competition = Competitions.query.get(id)
        db.session.delete(competition)
        db.session.commit()

        flash('Competition deleted.')
        return redirect(url_for('competitions'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            session['username'] = form.username.data
            flash('Login Successful.')
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():

    if 'username' not in session:
        redirect(url_for('login'))

    session.pop('username', None)

    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/teams', methods=['GET', 'POST'])
def teams():

    form = TeamForm()

    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']

    teams = db.session.query(Teams).order_by(Teams.number).all()

    if user is None:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            if not form.validate():
                return render_template('teams.html', teams=teams, form=form)
            else:
                newteam = Teams(number=form.number.data,
                                name=form.name.data,
                                timestamp=datetime.datetime.now())
                db.session.add(newteam)
                db.session.commit()

                flash('Team successfully added.')
                return redirect(url_for('teams'))

        elif request.method == 'GET':
            return render_template('teams.html', teams=teams, form=form)


@app.route('/teams/<int:id>', methods=['GET'])
def team(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user = session['username']
    if user is None:
        redirect(url_for('login'))
    else:
        team = db.session.query(Teams).filter(Teams.id == id).all()
        return render_template('team.html', id=id, team=team)


@app.route('/teams/delete/<int:id>', methods=['GET'])
def delete_team_entry(id):

    user = session['username']
    if user is None:
        return redirect(url_for('login'))
    else:
        team = Teams.query.get(id)
        db.session.delete(team)
        db.session.commit()

        flash('Team deleted.')
        return redirect(url_for('teams'))
