"""
username: viz
password: viz
 DB name: viz
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://viz:viz@localhost/viz'

img_dir = os.path.join(basedir, 'images')

SECRET_KEY = "viz"
