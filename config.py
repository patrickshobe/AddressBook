"""
Holds config info for app
"""

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Class that holds config vars"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
