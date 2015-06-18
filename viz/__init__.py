#!venv/bin/python
from flask import Flask, request, jsonify, render_template, url_for, abort, g
from flask.ext.wtf import Form
from wtforms import (TextField, IntegerField, SubmitField)
from wtforms.validators import Email, DataRequired
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.httpauth import HTTPBasicAuth
import logging, os

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

auth = HTTPBasicAuth()

from viz import models #, views
from models import UserDB, ImageDB


# Form for user creation, for development use
class UserForm(Form):
    """Testing purposes for db ease"""
    username = TextField('username')
    email = TextField('email')
    name = TextField('name')
    img_id = IntegerField('img_id')
    submit_button = SubmitField()

@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    form = UserForm()
    if request.method == 'POST':
        user = UserDB(username=form.username.data,
                      email=form.email.data,
                      name=form.name.data,
                      img_id=form.img_id.data)
        db.session.add(user)
        db.session.commit()
    return render_template("index.html", form=form)


# Testing a resource with login_required
@app.route('/api/resource')
@auth.login_required # Leads to verify_password decorator
def get_resource():
    return jsonify({'data': "Hello, %s!" % g.user.username})


# Route to get an authentication token
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode('ascii')})


# Get: return users with limit or offset fields.
# Post: user registration
@app.route('/api/users', methods=['POST','GET'])
@app.route('/api/users/', methods=['POST','GET'])
def users():
    if request.method == 'GET':
        lim = request.args.get('limit', 100)
        off = request.args.get('offset', 0)
        users = UserDB.query.limit(lim).offset(off).all()
        json_results = map(get_user_json, users)
        return jsonify(users=json_results)
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        name = request.json.get('name')
        if username is None or password is None:
            abort(400) # missing arguments
        if UserDB.query.filter_by(username=username).first() is not None:
            print "User", username, "exists in the database"
            abort(400) # existing user
        user = UserDB(username=username, email=email, name=name)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username}), 201, {'Location': url_for('user', username=user.username, _external=True)}


# Get a single user by username
@app.route('/api/users/<username>', methods=['GET'])
def user(username):
    if request.method == 'GET':
        user = UserDB.query.filter_by(username=username).first()
        return jsonify(user=get_user_json(user))


# Decorator for UserDB.verify_password
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate the token
    user = UserDB.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username and password
        user = UserDB.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# Return user's info including the path on the webserver to the user's profile picture
def get_user_json(user):
    img = ImageDB.query.filter_by(img_id=user.img_id).first()
    img_path = None
    if img:
        img_path = os.path.join('photos', user.username, img.img_name)
    return {'username': user.username,
            'name': user.name,
            'email': user.email,
            'img_path': img_path}
