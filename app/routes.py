from flask import render_template
from app import app
from app import db
from app.models import Address

@app.route('/')
def index():
    print(type(Address))
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)
