from flask_wtf import Form
from models import Competitions
from models import CompetitionTeam
from models import Teams
from models import Users
from wtforms import DateField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms_sqlalchemy.fields import QuerySelectField


class CompetitionsForm(Form):
    name = StringField('Name', [validators.DataRequired('Please enter the competition name.')])
    date = DateField('Date', [validators.DataRequired('Please enter the competition date.')], format='%Y-%m-%d')
    submit = SubmitField('Add Competition')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True


class CompetitionTeamForm(Form):
    competition = HiddenField('competition')
    team = QuerySelectField(query_factory=lambda: Teams.query.all(),
                            get_label='number')
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
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


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired('Please enter your username.')])
    password = PasswordField('Password', [validators.DataRequired('Please enter your password.')])
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = Users.query.filter_by(
            username=self.username.data.lower()).first()
        if user and user.verify_password(self.password.data):
            return True
        else:
            self.username.errors.append('Invalid username or password')
            return False


class TeamForm(Form):
    number = IntegerField('Number', [validators.DataRequired('Please enter the team number.')])
    name = StringField('Name', [validators.DataRequired('Please enter the team name.')])
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        checkteam = Teams.query.filter_by(number=self.number.data).first()
        if checkteam:
            self.number.errors.append("Team is already in the system.")
            return False
        else:
            return True
