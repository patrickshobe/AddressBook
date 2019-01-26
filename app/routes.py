from flask import render_template, flash, redirect
from app import app
from app import db
from app.models import Address
from app.forms import AddressForm

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)

@app.route('/address/new', methods=['GET', 'POST'])
def create():
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(name=form.name.data, address=form.address.data,
                          city = form.city.data, state = form.state.data,
                          zip = form.zip.data)
        db.session.add(address)
        db.session.commit()
        flash('{} Created Successfully'.format(form.name.data))
        return redirect('/')
    return render_template('create.html', form=form)
