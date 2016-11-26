from flask import Flask
from flask import g
from flask_bcrypt import Bcrypt
from flask_login import current_user
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)


@app.before_request
def _before_request():
    g.user = current_user
