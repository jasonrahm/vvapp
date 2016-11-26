from app.run import db
import os
import sys


sys.path.append(os.getcwd())

if __name__ == '__main__':
    db.create_all()
