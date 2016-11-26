from flask import Blueprint
routes = Blueprint('routes', __name__)

from .adduser import *
from .competitions import *
from .index import *
from .login import *
from .logout import *
from .users import *


