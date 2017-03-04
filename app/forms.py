from flask_wtf import FlaskForm
from models import Competitions
from models import CompetitionTeam
from models import Teams
from models import Users
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets import TextArea
from wtforms_sqlalchemy.fields import QuerySelectField


class CompetitionsForm(FlaskForm):
    name = StringField('Name',
                       [validators.DataRequired(
                           'Please enter the competition name.')])
    date = DateField('Date',
                     [validators.DataRequired(
                         'Please enter the competition date.')],
                     format='%Y-%m-%d')
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
    team = SelectField('Team', coerce=int)
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        super(CompetitionTeamForm, self).__init__(*args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        comp = Competitions.query.filter_by(name=self.competition).first()
        print self.team.data
        checkteam = CompetitionTeam.query.filter(
            (CompetitionTeam.competitions == comp.id) &
            (CompetitionTeam.teams == self.team.data)).first()
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


class MatchReportingForm(FlaskForm):
    a_center = SelectField('Center vortex (auto)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=3)
    a_center_miss = SelectField('Center vortex misses (auto)',
                                choices=[(0, 'Ignore'),
                                         (1, 'Important'),
                                         (3, 'Very Important'),
                                         (9, 'Critical')],
                                coerce=int,
                                default=0)

    a_beacons = SelectField('Beacons (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=3)
    a_beacons_miss = SelectField('Beacons missed (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=0)
    a_capball = SelectField('Capball Location (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    a_park = SelectField('Parking Location (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    t_center = SelectField('Center vortex (teleop)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=9)
    t_center_miss = SelectField('Center vortex misses (teleop)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=0)
    t_beacons = SelectField('Beacons claimed (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=9)
    t_beacons_pushed = SelectField('Beacons pushed (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=0)
    t_capball = SelectField('Capball Location (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    t_capball_tried = SelectField('Capball Attempted? (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=0)

    submit = SubmitField('Run Report')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        else:
            return True


class MatchScoringForm(FlaskForm):
    team = SelectField('Team', coerce=int)
    match_number = StringField('Match Number')
    a_center_vortex = IntegerField('Center Particles Scored', default=0)
    a_center_vortex_miss = IntegerField('Center Particles Missed', default=0)
    a_beacon = IntegerField('Beacons Claimed', default=0)
    a_beacon_miss = IntegerField('Beacons Missed', default=0)
    a_capball = SelectField('Cap Ball Location',
                            choices=[(0, 'Ball on Center'),
                                     (5, 'Ball on Floor')], coerce=int)
    a_park = SelectField('Robot Location',
                         choices=[(0, 'On the Floor'),
                                  (5, 'Partially on Center'),
                                  (10, 'Fully on Center'),
                                  (5, 'Partially on Corner'),
                                  (10, 'Fully on Corner')], coerce=int)
    t_center_vortex = IntegerField('Center Particles Scored', default=0)
    t_center_vortex_miss = IntegerField('Center Particles Missed', default=0)
    t_beacon = SelectField('Beacons Claimed',
                         choices=[(0, 'None'),
                                  (10, 'One'),
                                  (20, 'Two'),
                                  (30, 'Three'),
                                  (40, 'Four')], coerce=int)
    t_beacons_pushed = IntegerField('Beacons Pushed', default=0)
    t_capball = SelectField('Cap Ball Location',
                            choices=[(0, 'Floor'),
                                     (10, 'Elevated, < 30 inches'),
                                     (20, 'Elevated, > 30 inches'),
                                     (40, 'In Center Vortex')], coerce=int)
    t_capball_tried = BooleanField('Capball Attempted?')
    a_score = IntegerField('Autonomous Score', default=0)
    t_score = IntegerField('Teleop Score', default=0)
    total_score = IntegerField('Total Score', default=0)
    match_notes = StringField('Match Notes',
                              [validators.Length(
                                  max=500,
                                  message='Max length 500 characters.')],
                              widget=TextArea())

    submit = SubmitField('Add Score')

    def __init__(self, *args, **kwargs):
        super(MatchScoringForm, self).__init__(*args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #
    # def validate(self):
    #     if not Form.validate(self):
    #         return False


class PitReportingForm(FlaskForm):
    auto = SelectField('Autonomous',
                       choices=[(0, 'Ignore'),
                                (1, 'Important'),
                                (3, 'Very Important'),
                                (9, 'Critical')],
                       coerce=int,
                       default=1)
    auto_defense = SelectField('Defense (auto)',
                               choices=[(0, 'Ignore'),
                                        (1, 'Important'),
                                        (3, 'Very Important'),
                                        (9, 'Critical')],
                               coerce=int,
                               default=1)
    auto_compatible = SelectField('Compatible (auto)',
                                  choices=[(0, 'Ignore'),
                                           (1, 'Important'),
                                           (3, 'Very Important'),
                                           (9, 'Critical')],
                                  coerce=int,
                                  default=1)
    a_center = SelectField('Center vortex (auto)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=1)
    a_corner = SelectField('Corner vortex (auto)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=1)
    a_capball = SelectField('Capball (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    a_beacons = SelectField('Beacons (auto)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    a_park = SelectField('Parking position',
                         choices=[(0, 'Ignore'),
                                  (1, 'Important'),
                                  (3, 'Very Important'),
                                  (9, 'Critical')],
                         coerce=int,
                         default=1)
    t_center = SelectField('Center vortex (teleop)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=1)
    t_corner = SelectField('Corner vortex (teleop)',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (3, 'Very Important'),
                                    (9, 'Critical')],
                           coerce=int,
                           default=1)
    t_beacons = SelectField('Beacons (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)
    t_capball = SelectField('Capball (teleop)',
                            choices=[(0, 'Ignore'),
                                     (1, 'Important'),
                                     (3, 'Very Important'),
                                     (9, 'Critical')],
                            coerce=int,
                            default=1)

    submit = SubmitField('Run Report')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        else:
            return True


class PitScoutingForm(FlaskForm):
    team = SelectField('Team', coerce=int)
    drivetrain = SelectField('Type of Drivetrain',
                             choices=[(1, 'Skid Steer'),
                                      (2, 'Mechanum'),
                                      (3, 'Holonomic'),
                                      (4, 'Tank Treads'),
                                      (5, 'Unspecified')],
                             coerce=int,
                             default=5)
    auto = BooleanField('Do they have autonomous?')
    auto_defense = BooleanField('Do they play defense in autonomous?')
    auto_compatible = BooleanField('Is their autonomous compatible with ours?')
    a_center_balls = SelectField('Center vortex particles?',
                                 choices=[(0, 'No particles'),
                                          (1, '1 particle'),
                                          (2, '2 particles'),
                                          (3, '3+ particles')], coerce=int)
    a_corner_balls = SelectField('Corner vortex particles?',
                                 choices=[(0, 'No particles'),
                                          (1, '1 particle'),
                                          (2, '2 particles'),
                                          (3, '3+ particles')], coerce=int)
    a_capball = BooleanField('Can they knock the cap ball?')
    a_beacons = SelectField('Beacons Claimed?',
                                 choices=[(0, 'No beacons'),
                                          (1, '1 beacon'),
                                          (2, '2 beacons')], coerce=int)
    a_park = SelectField('Parking location?',
                                 choices=[(0, 'Floor'),
                                          (1, 'Partially on Center'),
                                          (1, 'Partially on Corner'),
                                          (2, 'Fully on Center'),
                                          (2, 'Fully on Corner')], coerce=int)
    t_center_balls = SelectField('Center vortex particles?',
                                 choices=[(0, 'No particles'),
                                          (1, '1-3 particles'),
                                          (2, '4-7 particles'),
                                          (3, '8+ particles')], coerce=int)
    t_corner_balls = SelectField('Corner vortex particles?',
                                 choices=[(0, 'No particles'),
                                          (1, '1-3 particles'),
                                          (2, '4-7 particles'),
                                          (3, '8+ particles')], coerce=int)
    t_beacons = BooleanField('Can they push beacons?')
    t_capball = SelectField('Can they lift the cap ball?',
                            choices=[(0, 'No'),
                                     (1, 'Low'),
                                     (2, 'High'),
                                     (3, 'Capped')], coerce=int)
    notes = StringField('Notes',
                        [validators.Length(
                            max=500,
                            message='Please limit to 500 characters.')],
                        widget=TextArea())

    submit = SubmitField('Add Scouting Report')

    def __init__(self, *args, **kwargs):
        super(PitScoutingForm, self).__init__(*args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]


class TeamForm(FlaskForm):
    number = IntegerField('Number',
                          [validators.DataRequired(
                              'Please enter the team number.')])
    name = StringField('Name',
                       [validators.DataRequired(
                           'Please enter the team name.')])
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
