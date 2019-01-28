from flask import render_template, flash, redirect
from app import app
from app import db
from app.models import Address
from app.forms import AddressForm
from app.address_validator import AddressValidator

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)

@app.route('/address/new', methods=['GET', 'POST'])
def create():
    form = AddressForm()
    if form.validate_on_submit():
        form_data = {'name': form.name.data,
                     'address': form.address.data,
                     'zip': form.zip.data,
                     'city': form.city.data,
                     'state': form.state.data,
                        }
        validator = AddressValidator(form_data)
        validator.request()
        flash('{} Created Successfully'.format(form.name.data))
        return redirect('/')
    return render_template('create.html', form=form)

@app.route('/address/delete/<int:id>')
def delete(id):
    Address.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Entry Successfully Deleted')
    return redirect('/')

