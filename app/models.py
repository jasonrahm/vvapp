from passlib.apps import custom_app_context as pwd_context
from app import db
import datetime


class Competitions(db.Model):
    __tablename__ = 'Competitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self, name, date, timestamp):
        self.name = name
        self.date = date
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<Competition %r>' % self.id


class CompetitionTeam(db.Model):
    __tablename__ = 'CompetitionTeams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'),
                             nullable=False,
                             index=True)
    teams = db.Column(db.ForeignKey('Teams.id'), nullable=False, index=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self, competitions, teams, timestamp):
        self.competitions = competitions
        self.teams = teams
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<CompetitionTeam %r %r %r>' % (self.id,
                                               self.competitions,
                                               self.teams)


class Teams(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self,
                 number,
                 name,
                 timestamp):
        self.number = number
        self.name = name
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<Team %r %r %r>' % (self.id, self.number, self.name)


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, username, password_hash, role, timestamp):
        self.username = username
        self.password_hash = pwd_context.encrypt(password_hash)
        self.role = role
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<Users %r>' % self.username
