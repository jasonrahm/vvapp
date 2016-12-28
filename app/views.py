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
from forms import MatchScoringForm
from forms import PitScoutingForm
from forms import TeamForm
from models import db
from models import Competitions
from models import CompetitionTeam
from models import MatchScore
from models import PitScouting
from models import Teams
from models import Users
from sqlalchemy import and_

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


@app.route('/competitions/<int:comp_id>/delete/<int:team_id>', methods=['GET'])
@login_required
def delete_team_from_comp(comp_id, team_id):
    team = Teams.query.get(team_id)
    records = CompetitionTeam.query.filter(and_(
        CompetitionTeam.competitions == comp_id,
        CompetitionTeam.teams == team_id)).first()
    db.session.delete(records)
    db.session.commit()
    flash('Team {0} deleted from competition'.format(team.name))
    return redirect(url_for('manage_competition', id=comp_id))


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


@app.route('/match-scoring', methods=['GET', 'POST'])
@login_required
def match_scoring():
    form = MatchScoringForm(request.values)
    form.competition.choices = [(a.id, a.name) for a in
                                Competitions.query.order_by('name')]
    form.team.choices = [(a.id, a.number) for a in
                         Teams.query.order_by('number')]

    if request.method == 'POST':
        if not form.validate():
            return render_template('match_scoring.html', form=form)
        else:
            competition = request.form.get('competition', '')
            team = request.form.get('team', '')
            match_number = request.form.get('match_number', '')
            a_center_vortex = request.form.get('a_center_vortex', '')
            a_corner_vortex = request.form.get('a_corner_vortex', '')
            a_beacon = request.form.get('a_beacon', '')
            a_capball = request.form.get('a_capball', '')
            a_park = request.form.get('a_park', '')
            t_center_vortex = request.form.get('t_center_vortex', '')
            t_corner_vortex = request.form.get('t_corner_vortex', '')
            t_beacon = request.form.get('t_beacon', '')
            t_capball = request.form.get('t_capball', '')
            a_score = request.form.get('a_score', '')
            t_score = request.form.get('t_score', '')
            total_score = request.form.get('total_score', '')
            particle_speed = request.form.get('particle_speed', '')
            capball_speed = request.form.get('capball_speed', '')
            match_notes = request.form.get('match_notes', '')

            matchscore = MatchScore(
                teams=team,
                competitions=competition,
                match_number=match_number,
                a_center_vortex=a_center_vortex,
                a_corner_vortex=a_corner_vortex,
                a_beacon=a_beacon,
                a_capball=a_capball,
                a_park=a_park,
                t_center_vortex=t_center_vortex,
                t_corner_vortex=t_corner_vortex,
                t_beacon=t_beacon,
                t_capball=t_capball,
                a_score=a_score,
                t_score=t_score,
                total_score=total_score,
                particle_speed=particle_speed,
                capball_speed=capball_speed,
                match_notes=match_notes,
                timestamp=datetime.datetime.now())
            db.session.add(matchscore)
            db.session.commit()

            flash('Score Added Successfully')
            return redirect(url_for('match_scoring'))

    elif request.method == 'GET':
        return render_template('match_scoring.html', form=form)


@app.route('/pit-scouting/', defaults={'comp': 2}, methods=['GET', 'POST'])
@app.route('/pit-scouting/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def pit_scouting(comp):
    form = PitScoutingForm(request.values)

    sql_text = '''SELECT *
      FROM
        CompetitionTeams ct
      INNER JOIN
        Teams t ON ct.teams = t.id
      WHERE
        ct.competitions = {}'''.format(comp)
    result = db.engine.execute(sql_text)

    form.team.choices = [(a.id, a.number) for a in result]

    if request.method == 'POST':
        if not form.validate():
            return render_template('pit_scouting.html', form=form)
        else:
            # Put Code to process form and add to DB here
            team = request.form.get('team', '')
            drivetrain = request.form.get('drivetrain', '')
            auto = request.form.get('auto', '')
            auto_defense = request.form.get('auto_defense', '')
            auto_compatible = request.form.get('auto_compatible', '')
            a_center_balls = request.form.get('a_center_balls', '')
            a_corner_balls = request.form.get('a_corner_balls', '')
            a_capball = request.form.get('a_capball', '')
            a_beacons = request.form.get('a_beacons', '')
            a_park = request.form.get('a_park', '')
            t_center_balls = request.form.get('t_center_balls', '')
            t_corner_balls = request.form.get('t_corner_balls', '')
            t_beacons = request.form.get('t_beacons', '')
            t_capball = request.form.get('t_capball', '')
            notes = request.form.get('notes', '')
            watchlist = request.form.get('watchlist', '')

            pitscouting = PitScouting(
                competitions=comp,
                teams=team,
                drivetrain=drivetrain,
                auto=auto,
                auto_defense=auto_defense,
                auto_compatible=auto_compatible,
                a_center_balls=a_center_balls,
                a_corner_balls=a_corner_balls,
                a_capball=a_capball,
                a_beacons=a_beacons,
                a_park=a_park,
                t_center_balls=t_center_balls,
                t_corner_balls=t_corner_balls,
                t_beacons=t_beacons,
                t_capball=t_capball,
                notes=notes,
                watchlist=watchlist,
                timestamp=datetime.datetime.now())

            db.session.add(pitscouting)
            db.session.commit()

            flash('Pit scouting data added successfully')
            return redirect(url_for('pit_scouting'))

    elif request.method == 'GET':
        return render_template('pit_scouting.html', form=form)


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
    competitions = db.session.query(Competitions).filter(Teams.id == id).all()

    return render_template('team.html',
                           id=id,
                           team=team,
                           competitions=competitions)


@app.route('/teams/<int:team_id>/comp/<int:comp_id>', methods=['GET'])
@login_required
def team_scores_by_comp(team_id, comp_id):
    team = db.session.query(Teams).filter(Teams.id == team_id).all()
    comp = db.session.query(
        Competitions).filter(Competitions.id == comp_id).all()
    match_scores = db.session.query(
        MatchScore).filter(
        and_(Teams.id == team_id, Competitions.id == comp_id)).all()
    pit_scouting = db.session.query(
        PitScouting).filter(
        and_(Teams.id == team_id, Competitions.id == comp_id)).all()

    return render_template('team_scores.html',
                           team_id=team_id,
                           comp_id=comp_id,
                           team=team,
                           comp=comp,
                           match_scores=match_scores,
                           pit_scouting=pit_scouting)


@app.route('/teams/delete/<int:id>', methods=['GET'])
@login_required
def delete_team_entry(id):

    team = Teams.query.get(id)
    db.session.delete(team)
    db.session.commit()

    flash('Team deleted.')
    return redirect(url_for('teams'))
