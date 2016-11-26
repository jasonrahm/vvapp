from app import bcrypt
from app import db
from app import login_manager
from slugify import slugify
import datetime


@login_manager.user_loader
def _user_loader(user_id):
    return Users.query.get(int(user_id))


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
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(unicode(self.name, "utf-8"))

    def __repr__(self):
        return '<Users %r>' % self.email

    # Start Flask-Login interface methods
    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return Users(
            email=email,
            password_hash=Users.make_password(password),
            **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = Users.query.filter(Users.email == email).first()
        if user and user.check_password(password):
            return user
        return False

