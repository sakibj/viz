#!venv/bin/python
from viz import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"
