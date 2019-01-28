""" Defines Forms """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddressForm(FlaskForm):
    """ Defines the new address form """
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State',
                        validators=[DataRequired(),
                                    Length(min=2,
                                           max=2,
                                        message='State should be abbreviated')])
    zip = StringField('Zip', validators=[DataRequired()])
    submit = SubmitField('Submit')
