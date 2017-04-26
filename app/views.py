from app import app
from app import login_manager
from BeautifulSoup import BeautifulSoup as bs
from flask import abort
from flask import flash
from flask import Markup
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
from forms import MatchReportingForm
from forms import MatchScoringForm
from forms import PitReportingForm
from forms import PitScoutingForm
from forms import TeamForm
# import json
from models import db
from models import Competitions
from models import CompetitionTeam
from models import MatchScore
from models import PitScouting
from models import Teams
from models import Users
from pytz import timezone
import requests
from sqlalchemy import and_

import datetime

today = datetime.datetime.now(timezone('America/Chicago')).strftime("%Y-%m-%d")
compcheck = db.session.query(Competitions).filter(
    Competitions.date == today).first()
if compcheck is not None:
    cur_comp = compcheck.id
else:
    cur_comp = 7

print cur_comp

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


@app.route('/match-list/', methods=['GET'])
def match_list():
    ml = 'http://firstinspiresiowa.org/cache/' \
         'Matches_North_Super_Regional_Kindig.html'
    ml_response = requests.get(ml, verify=False)
    ml_soup = bs(ml_response.text)
    ml_data = ml_soup.findAll('table')[0]

    return render_template('matchlist.html',
                           ml_data=Markup(ml_data))


@app.route('/match-report/', methods=['GET'])
@login_required
def match_report():
    data = session['matchreport']
    if data =='':
        redirect(url_for(match_reporting))
    else:
        return render_template('match_report.html', data=data)


@app.route('/match-reporting/', defaults={'comp': cur_comp}, methods=['GET', 'POST'])
@app.route('/match-reporting/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def match_reporting(comp):

    form = MatchReportingForm(request.values)

    if request.method == 'POST':
        if not form.validate():
            return render_template('match_reporting.html', form=form)
        else:
            postdata = request.values
            teams_scored = db.session.query(MatchScore.teams).filter(
                MatchScore.competitions == comp).distinct()
            teams = []
            for x in teams_scored:
                sql_text = '''select Teams.name, Teams.number,
                           avg(total_score), max(total_score),
                           (avg(a_center_vortex)*15*%d) +
                           (avg(a_beacon)*30*%d) +
                           (avg(a_capball)*%d) +
                           (avg(a_park)*%d) +
                           (avg(t_center_vortex)*5*%d) +
                           (avg(t_beacon)*%d) +
                           (avg(t_capball)*%d)
                           AS Score
                           FROM MatchScore
                           INNER JOIN Teams
                             On MatchScore.teams = Teams.id
                           WHERE competitions = %d AND teams = %d
                           ORDER BY Score
                           DESC''' % (int(postdata['a_center']),
                                      int(postdata['a_beacons']),
                                      int(postdata['a_capball']),
                                      int(postdata['a_park']),
                                      int(postdata['t_center']),
                                      int(postdata['t_beacons']),
                                      int(postdata['t_capball']),
                                      comp,
                                      x[0])
                result = db.engine.execute(sql_text)
                for row in result:
                    teams.append([row[0], row[1], row[2], row[3], row[4]])
            session['matchreport'] = teams

            flash('Report Ran Successfully.')
            return redirect(url_for('match_report'))

    elif request.method == 'GET':
        return render_template('match_reporting.html', form=form)


@app.route('/match-scoring/', defaults={'comp': cur_comp}, methods=['GET', 'POST'])
@app.route('/match-scoring/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def match_scoring(comp):
    form = MatchScoringForm(request.values)

    sql_text = '''SELECT *
          FROM
            CompetitionTeams ct
          INNER JOIN
            Teams t ON ct.teams = t.id
          WHERE
            ct.competitions = {}
          ORDER BY t.number ASC'''.format(comp)
    result = db.engine.execute(sql_text)

    form.team.choices = [(a.id,
                          "{}: {}".format(a.number, a.name)) for a in result]

    if request.method == 'POST':
        if not form.validate():
            return render_template('match_scoring.html', form=form)
        else:
            team = request.form.get('team', '')
            match_number = request.form.get('match_number', '')
            a_center_vortex = request.form.get('a_center_vortex', '')
            a_center_vortex_miss = request.form.get('a_center_vortex_miss', '')
            a_beacon = request.form.get('a_beacon', '')
            a_beacon_miss = request.form.get('a_beacon_miss', '')
            a_capball = request.form.get('a_capball', '')
            a_park = request.form.get('a_park', '')
            t_center_vortex = request.form.get('t_center_vortex', '')
            t_center_vortex_miss = request.form.get('t_center_vortex_miss', '')
            t_beacon = request.form.get('t_beacon', '')
            t_beacons_pushed = request.form.get('t_beacons_pushed', '')
            t_capball = request.form.get('t_capball', '')
            t_capball_tried = request.form.get('t_capball_tried', '')
            a_score = request.form.get('a_score', '')
            t_score = request.form.get('t_score', '')
            total_score = request.form.get('total_score', '')
            match_notes = request.form.get('match_notes', '')

            matchscore = MatchScore(
                teams=team,
                competitions=comp,
                match_number=match_number,
                a_center_vortex=a_center_vortex,
                a_center_vortex_miss=a_center_vortex_miss,
                a_corner_vortex=0,
                a_beacon=a_beacon,
                a_beacon_miss=a_beacon_miss,
                a_capball=a_capball,
                a_park=a_park,
                t_center_vortex=t_center_vortex,
                t_center_vortex_miss=t_center_vortex_miss,
                t_corner_vortex=0,
                t_beacon=t_beacon,
                t_beacons_pushed=t_beacons_pushed,
                t_capball=t_capball,
                t_capball_tried=t_capball_tried,
                a_score=a_score,
                t_score=t_score,
                total_score=total_score,
                particle_speed=0,
                capball_speed=0,
                match_notes=match_notes,
                timestamp=datetime.datetime.now())
            db.session.add(matchscore)
            db.session.commit()

            flash('Score Added Successfully')
            return redirect(url_for('match_scoring'))

    elif request.method == 'GET':
        matches = db.session.query(MatchScore).filter(
            MatchScore.competitions == comp).all()
        return render_template('match_scoring.html',
                               action='Add', form=form, matches=matches)


@app.route('/match/<int:match_id>/delete', methods=['GET'])
@login_required
def match_delete(match_id):
    match = db.session.query(MatchScore).get(match_id)
    if match is None:
        abort(404)
    db.session.delete(match)
    db.session.commit()

    flash('Match deleted.')
    return redirect(url_for('match_scoring'))


@app.route('/match/<int:match_id>/edit', methods=['GET', 'POST'])
@login_required
def match_edit(match_id):
    match = db.session.query(MatchScore).get(match_id)
    if match is None:
        abort(404)
    form = MatchScoringForm(request.values, obj=match)
    form.team.choices = [
            (a.id, a.number) for a in Teams.query.filter(
            Teams.id == match.teams)]
    if request.method == 'POST' and form.validate_on_submit():
        postdata = request.values
        t_capball_tried = True if 't_capball' in request.form else False
        sql_text = '''update MatchScore set match_number="%s", \
                        a_center_vortex=%d, \
                        a_center_vortex_miss=%d, \
                        a_beacon=%d, \
                        a_beacon_miss=%d, \
                        a_capball=%d, \
                        a_park=%d, \
                        t_center_vortex=%d, \
                        t_center_vortex_miss=%d, \
                        t_beacon=%d, \
                        t_beacons_pushed=%d, \
                        t_capball=%d, \
                        t_capball_tried=%d, \
                        a_score=%d, \
                        t_score=%d, \
                        total_score=%d, \
                        match_notes="%s" where id = %d''' % (
            str(postdata['match_number']),
            int(postdata['a_center_vortex']),
            int(postdata['a_center_vortex_miss']),
            int(postdata['a_beacon']),
            int(postdata['a_beacon_miss']),
            int(postdata['a_capball']),
            int(postdata['a_park']),
            int(postdata['t_center_vortex']),
            int(postdata['t_center_vortex_miss']),
            int(postdata['t_beacon']),
            int(postdata['t_beacons_pushed']),
            int(postdata['t_capball']),
            t_capball_tried,
            int(postdata['a_score']),
            int(postdata['t_score']),
            int(postdata['total_score']),
            str(postdata['match_notes']),
            match_id)
        result = db.engine.execute(sql_text)
        # form.populate_obj(match)
        # db.session.commit()
        flash('Score Updated Successfully')
        return redirect(url_for('match_edit', match_id=match_id))
    elif request.method == 'GET':
        return render_template('match.html',
                               form=form,
                               match=match)


@app.route('/pit-report', methods=['GET'])
@login_required
def pit_report():
    data = session['pitreport']
    if data == '':
        redirect(url_for(pit_reporting))
    else:
        return render_template('pit_report.html', data=data)


@app.route('/pit-report/<int:id>')
@login_required
def get_pit_report(id):
    data = PitScouting.query.get(id)
    return render_template('pit_report_details.html', data=data)


@app.route('/pit-reporting/', defaults={'comp': cur_comp}, methods=['GET', 'POST'])
@app.route('/pit-reporting/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def pit_reporting(comp):

    form = PitReportingForm(request.values)

    if request.method == 'POST':
        if not form.validate():
            return render_template('pit_reporting.html', form=form)
        else:
            postdata = request.values
            sql_text = '''select PitScouting.id, Teams.name, Teams.number,
                            (auto*%d) +
                            (auto_defense*%d) +
                            (auto_compatible*%d) +
                            (a_center_balls*%d) +
                            (a_corner_balls*%d) +
                            (a_capball*%d) +
                            (a_beacons*%d) +
                            (a_park*%d) +
                            (t_center_balls*%d) +
                            (t_corner_balls*%d) +
                            (t_beacons*%d) +
                            (t_capball*%d)
                          As Score, PitScouting.Competitions
                          FROM PitScouting
                          INNER JOIN Teams
                            On PitScouting.teams = Teams.id
                          WHERE competitions = %d
                          ORDER BY Score
                          DESC ''' % (int(postdata['auto']),
                                      int(postdata['auto_defense']),
                                      int(postdata['auto_compatible']),
                                      int(postdata['a_center']),
                                      int(postdata['a_corner']),
                                      int(postdata['a_capball']),
                                      int(postdata['a_beacons']),
                                      int(postdata['a_park']),
                                      int(postdata['t_center']),
                                      int(postdata['t_corner']),
                                      int(postdata['t_beacons']),
                                      int(postdata['t_capball']),
                                      comp)
            result = db.engine.execute(sql_text)
            teams = []
            for row in result:
                teams.append([row[0], row[1], row[2], row[3], row[4]])

            session['pitreport'] = teams

            flash('Report Ran Successfully.')
            return redirect(url_for('pit_report'))

    elif request.method == 'GET':
        return render_template('pit_reporting.html', form=form)


@app.route('/pit-scouting/', defaults={'comp': cur_comp}, methods=['GET', 'POST'])
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
        ct.competitions = {}
      ORDER BY t.number ASC'''.format(comp)
    result = db.engine.execute(sql_text)

    form.team.choices = [(a.id,
                          "{}: {}".format(a.number, a.name)) for a in result]

    if request.method == 'POST':
        if not form.validate():
            return render_template('pit_scouting.html', form=form)
        else:
            # Put Code to process form and add to DB here
            team = request.form.get('team', '')
            adv = request.form.get('adv', '')
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
            # removed from form; setting to empty
            watchlist = ''

            pitscouting = PitScouting(
                competitions=comp,
                teams=team,
                adv=adv,
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


@app.route('/rankings', methods=['GET'])
def rankings():
    rank = 'http://firstinspiresiowa.org/cache/' \
           'Rankings_North_Super_Regional_Kindig.html'
    rank_response = requests.get(rank, verify=False)
    rank_soup = bs(rank_response.text)
    rank_data = rank_soup.findAll('table')[0]

    match = 'http://firstinspiresiowa.org/cache/' \
            'MatchResults_North_Super_Regional_Kindig.html'
    match_response = requests.get(match, verify=False)
    match_soup = bs(match_response.text)
    match_data = match_soup.findAll('table')[0]

    # matchdetails = 'http://firstinspiresiowa.org/cache/' \
    #                'MatchResultsDetails_North_Super_Regional_Kindig.html'
    # matchdetails_response = requests.get(matchdetails, verify=False)
    # matchdetails_soup = bs(matchdetails_response.text)
    # matchdetails_data = matchdetails_soup.findAll('table')[0]

    return render_template('rankings.html',
                           rank_data=Markup(rank_data),
                           match_data=Markup(match_data))
                           # matchdetails_data=Markup(matchdetails_data))


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

    # # Get MoFTCData
    # req = requests.session()
    # req.headers.update({'Content-Type': 'application/json'})
    # team_data = req.get('http://moftcscores.net/api/v1/team/{}'.format(team[0].number)).json()
    # for item in team_data.get('games'):
    #     if item.get('game_id') == 'velocity':
    #         vvdata = item

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
        and_(MatchScore.teams == team_id,
             MatchScore.competitions == comp_id)).all()
    pit_scouting = db.session.query(
        PitScouting).filter(
        and_(PitScouting.teams == team_id,
             PitScouting.competitions == comp_id)).all()

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
