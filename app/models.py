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


class MatchScore(db.Model):
    __tablename__ = 'MatchScores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teams = db.Column(db.ForeignKey('Teams.id'), index=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'), index=True)
    match_number = db.Column(db.String)
    a_center_vortex = db.Column(db.Integer)
    a_corner_vortex = db.Column(db.Integer)
    a_beacon = db.Column(db.Integer)
    a_capball = db.Column(db.Integer)
    a_park = db.Column(db.Integer)
    t_center_vortex = db.Column(db.Integer)
    t_corner_vortex = db.Column(db.Integer)
    t_beacon = db.Column(db.Integer)
    t_capball = db.Column(db.Integer)
    a_score = db.Column(db.Integer)
    t_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    particle_speed = db.Column(db.Integer)
    capball_speed = db.Column(db.Integer)
    match_notes = db.Column(db.String(500))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self,
                 teams,
                 competitions,
                 match_number,
                 a_center_vortex,
                 a_corner_vortex,
                 a_beacon,
                 a_capball,
                 a_park,
                 t_center_vortex,
                 t_corner_vortex,
                 t_beacon,
                 t_capball,
                 a_score,
                 t_score,
                 total_score,
                 particle_speed,
                 capball_speed,
                 match_notes,
                 timestamp):
        self.teams = teams
        self.competitions = competitions
        self.match_number = match_number
        self.a_center_vortex = a_center_vortex
        self.a_corner_vortex = a_corner_vortex
        self.a_beacon = a_beacon
        self.a_capball = a_capball
        self.a_park = a_park
        self.t_center_vortex = t_center_vortex
        self.t_corner_vortex = t_corner_vortex
        self.t_beacon = t_beacon
        self.t_capball = t_capball
        self.a_score = a_score
        self.t_score = t_score
        self.total_score = total_score
        self.particle_speed = particle_speed
        self.capball_speed = capball_speed
        self.match_notes = match_notes
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<MatchScore %r %r %r>' % (self.id, self.teams, self.total_score)


class PitScouting(db.Model):
    __tablename__ = 'PitScouting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teams = db.Column(db.ForeignKey('Teams.id'), index=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'), index=True)
    drivetrain = db.Column(db.String(50))
    auto = db.Column(db.Boolean)
    auto_defense = db.Column(db.Boolean)
    auto_compatible = db.Column(db.Boolean)
    a_center_balls = db.Column(db.Integer)
    a_corner_balls = db.Column(db.Integer)
    a_capball = db.Column(db.Boolean)
    a_beacons = db.Column(db.Integer)
    a_park = db.Column(db.Boolean)
    t_center_balls = db.Column(db.Integer)
    t_corner_balls = db.Column(db.Integer)
    t_beacons = db.Column(db.Boolean)
    t_capball = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    watchlist = db.Column(db.Boolean)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self,
                 teams,
                 competitions,
                 drivetrain,
                 auto,
                 auto_defense,
                 auto_compatible,
                 a_center_balls,
                 a_corner_balls,
                 a_capball,
                 a_beacons,
                 a_park,
                 t_center_balls,
                 t_corner_balls,
                 t_beacons,
                 t_capball,
                 notes,
                 watchlist,
                 timestamp):
        self.teams = teams
        self.competitions = competitions
        self.drivetrain = drivetrain
        self.auto = auto
        self.auto_defense = auto_defense
        self.auto_compatible = auto_compatible
        self.a_center_balls = a_center_balls
        self.a_corner_balls = a_corner_balls
        self.a_capball = a_capball
        self.a_beacons = a_beacons
        self.a_park = a_park
        self.t_center_balls = t_center_balls
        self.t_corner_balls = t_corner_balls
        self.t_beacons = t_beacons
        self.t_capball = t_capball
        self.notes = notes
        self.watchlist = watchlist
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<PitScouting %r %r %r>' % (self.id,
                                           self.teams,
                                           self.competitions)


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

