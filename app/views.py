from app import app
from app import login_manager
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from forms import CompetitionsForm
from forms import CompetitionTeamForm
from forms import LoginForm
from forms import TeamForm
from models import db
from models import Competitions
from models import CompetitionTeam
from models import Teams
from models import Users

import datetime


@app.errorhandler(404)
def missing_file(error):
    return render_template('servererror.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/competitions', methods=['GET', 'POST'])
@login_required
def competitions():

    form = CompetitionsForm()

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
@login_required
def manage_competition(id):

    form = CompetitionTeamForm(request.values, competition=id)
    comp = Competitions.query.get(id)
    form.competition = comp.name
    form.team.choices = [(a.id, a.number) for a in Teams.query.all()]

    teams = db.session.query(CompetitionTeam).filter(
        CompetitionTeam.competitions == id).all()
    team_list = []
    for team in teams:
        team_list.append(int(team.teams))
    team_data = db.session.query(Teams).filter(
        Teams.id.in_(team_list)).order_by(Teams.number).all()

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
@login_required
def delete_competition_entry(id):

    competition = Competitions.query.get(id)
    db.session.delete(competition)
    db.session.commit()

    flash('Competition deleted.')
    return redirect(url_for('competitions'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user = Users.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember_me.data)
            flash('Login Successful.')
            return redirect(request.args.get('next') or url_for('index'))
    else:
        form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():

    form = TeamForm()

    teams = db.session.query(Teams).order_by(Teams.number).all()

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
@login_required
def team(id):

    team = db.session.query(Teams).filter(Teams.id == id).all()
    return render_template('team.html', id=id, team=team)


@app.route('/teams/delete/<int:id>', methods=['GET'])
@login_required
def delete_team_entry(id):

    team = Teams.query.get(id)
    db.session.delete(team)
    db.session.commit()

    flash('Team deleted.')
    return redirect(url_for('teams'))
