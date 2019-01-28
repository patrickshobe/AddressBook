""" Defines Application Routes """
from flask import render_template, flash, redirect
from app import app
from app import db
from app.models import Address
from app.forms import AddressForm, ZipForm
from app.address_validator import ZipService


@app.route('/')
@app.route('/addresses')
def index():
    """ Address Index """
    addresses = Address.query.order_by('address.name')
    return render_template('index.html', addresses=addresses)


@app.route('/addresses/new', methods=['GET', 'POST'])
def create():
    """ Address New """
    form = AddressForm()
    if form.validate_on_submit():
        form_data = {'name': form.name.data,
                     'address': form.address.data,
                     'zip': form.zip.data,
                     'city': form.city.data,
                     'state': form.state.data}
        validator = ZipService()
        validator.validate_address(form_data)
        flash('{} Created Successfully'.format(form.name.data))
        return redirect('/')
    return render_template('create.html', form=form)


@app.route('/addresses/delete/<int:id>')
def delete(id):
    """ Address Delete """
    Address.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Entry Successfully Deleted')
    return redirect('/addresses')

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    """ Lookup Route """
    form = ZipForm()
    if form.validate_on_submit():
        zip_service = ZipService()
        response = zip_service.perform_lookup(form.zip.data)
        return render_template('lookup.html', form=form, result=response)
    return render_template('lookup.html', result=None, form=form)
