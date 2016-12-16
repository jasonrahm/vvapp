from flask_wtf import FlaskForm
from models import Competitions
from models import CompetitionTeam
from models import Teams
from models import Users
from wtforms import BooleanField
from wtforms.fields.html5 import DateField
from wtforms import HiddenField
from wtforms.fields.html5 import IntegerField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms_sqlalchemy.fields import QuerySelectField


class CompetitionsForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired('Please enter the competition name.')])
    date = DateField('Date', [validators.DataRequired('Please enter the competition date.')], format='%Y-%m-%d')
    submit = SubmitField('Add Competition')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        else:
            return True


class CompetitionTeamForm(FlaskForm):
    competition = HiddenField('competition')
    team = QuerySelectField(query_factory=lambda: Teams.query.all(),
                            get_label='number')
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        comp = Competitions.query.filter_by(name=self.competition).first()
        checkteam = CompetitionTeam.query.filter(
            (CompetitionTeam.competitions == comp.id) &
            (CompetitionTeam.teams == self.team.data.id)).first()
        if checkteam:
            self.team.errors.append("Team is already part of this competition")
            return False
        else:
            return True


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField("Remember me?", default=True)
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = Users.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password")
            return False

        return True


class MatchScoringForm(FlaskForm):
    competition = QuerySelectField(
        query_factory=lambda: Competitions.query.all(), get_label='name')
    team = QuerySelectField(
        query_factory=lambda: Teams.query.all(), get_label='number')
    match_number = StringField('Match Number')
    a_center_vortex = IntegerField('Center Vortex Score', default=0)
    a_corner_vortex = IntegerField('Corner Vortex Score', default=0)
    a_beacon = IntegerField('Beacon Score', default=0)
    a_capball = SelectField('Cap Ball Location',
                            choices=[(0, 'Ball on Center'),
                                     (5, 'Ball on Floor')], coerce=int)
    a_park = SelectField('Robot Location',
                         choices=[(0, 'On the Floor'),
                                  (5, 'Partially on Center'),
                                  (10, 'Fully on Center'),
                                  (5, 'Partially on Corner'),
                                  (10, 'Fully on Corner')], coerce=int)
    t_center_vortex = IntegerField('Center Vortex Score', default=0)
    t_corner_vortex = IntegerField('Corner Vortex Score', default=0)
    t_beacon = SelectField('Beacons Claimed',
                           choices=[(0, 'None'),
                                    (10, 'One'),
                                    (20, 'Two'),
                                    (30, 'Three'),
                                    (40, 'Four')], coerce=int)
    t_capball = SelectField('Cap Ball Location',
                            choices=[(0, 'Floor'),
                                     (10, 'Elevated, < 30 inches'),
                                     (20, 'Elevated, > 30 inches'),
                                     (40, 'In Center Vortext')], coerce=int)
    a_score = IntegerField('Autonomous Score', default=0)
    t_score = IntegerField('Teleop Score', default=0)
    total_score = IntegerField('Total Score', default=0)
    adv_metrics = BooleanField('Advanced Scoring?', default=False)
    particle_speed = SelectField('Particle Collection Speed',
                                 choices=[(0, 'Less than 10s'),
                                          (1, 'Between 10-15s'),
                                          (2, 'More than 15s')], coerce=int)
    capball_speed = SelectField('Cap Ball Collection Speed',
                                choices=[(0, 'Less than 10s'),
                                         (1, 'Between 10-20s'),
                                         (2, 'More than 20s')], coerce=int
                                )
    match_notes = StringField('Match Notes', [validators.Length(max=500, message='Max length 500 characters.')])

    submit = SubmitField('Add Score')

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #
    # def validate(self):
    #     if not Form.validate(self):
    #         return False


class PitScoutingForm(FlaskForm):
    competition = QuerySelectField(
        query_factory=lambda: Competitions.query.all(), get_label='name')
    team = QuerySelectField(
        query_factory=lambda: Teams.query.all(), get_label='number')
    a_canScoreCenter = BooleanField('Can you launch in the center vortex?')
    a_canScoreCorner = BooleanField('Can you launch in the corner vortex?')
    a_canMoveBall = BooleanField('Can you move the ball?')
    a_canPushBeacons = BooleanField('Can you push beacons?')
    a_canParkCenter = BooleanField('Can you park in the center?')
    a_canParkCorner = BooleanField('Can you park in the corner?')
    t_canScoreCenter = BooleanField('Can you launch in the center vortex?')
    t_canScoreCorner = BooleanField('Can you launch in the corner vortex?')
    t_canPushBeacons = BooleanField('Can you push beacons?')
    t_canLiftBall = BooleanField('Can you lift the ball?')
    notes = StringField('Notes', [validators.Length(max=500, message='Please limit to 500 characters.')])
    watchlist = BooleanField('Add to watchlist?')

    submit = SubmitField('Add Pit Report')


class TeamForm(FlaskForm):
    number = IntegerField('Number', [validators.DataRequired('Please enter the team number.')])
    name = StringField('Name', [validators.DataRequired('Please enter the team name.')])
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        checkteam = Teams.query.filter_by(number=self.number.data).first()
        if checkteam:
            self.number.errors.append("Team is already in the system.")
            return False
        else:
            return True
