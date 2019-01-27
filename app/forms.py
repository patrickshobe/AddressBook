from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length

class AddressForm(FlaskForm):
    addresses = [('Alabama',  'AL'), ('Alaska',  'AK'), ('Arizona',  'AZ'),
                 ('Arkansas',  'AR'), ('California',  'CA'),
                 ('Colorado',  'CO'), ('Connecticut',  'CT'),
                 ('Delaware',  'DE'), ('Florida',  'FL'), ('Georgia',  'GA'),
                 ('Hawaii',  'HI'), ('Idaho',  'ID'), ('Illinois',  'IL'),
                 ('Indiana',  'IN'), ('Iowa',  'IA'), ('Kansas',  'KS'),
                 ('Kentucky',  'KY'), ('Louisiana',  'LA'), ('Maine',  'ME'),
                 ('Maryland',  'MD'), ('Massachusetts',  'MA'),
                 ('Michigan',  'MI'), ('Minnesota',  'MN'),
                 ('Mississippi',  'MS'), ('Missouri',  'MO'),
                 ('Montana',  'MT'), ('Nebraska',  'NE'), ('Nevada',  'NV'),
                 ('New Hampshire',  'NH'), ('New Jersey',  'NJ'),
                 ('New Mexico',  'NM'), ('New York',  'NY'),
                 ('North Carolina',  'NC'), ('North Dakota',  'ND'),
                 ('Ohio',  'OH'), ('Oklahoma',  'OK'), ('Oregon',  'OR'),
                 ('Pennsylvania',  'PA'), ('Rhode Island',  'RI'),
                 ('South Carolina',  'SC'), ('South Dakota',  'SD'),
                 ('Tennessee',  'TN'), ('Texas',  'TX'), ('Utah',  'UT'),
                 ('Vermont',  'VT'), ('Virginia',  'VA'), ('Washington',  'WA'),
                 ('West Virginia',  'WV'), ('Wisconsin',  'WI'),
                 ('Wyoming',  'WY')]
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=2, message='State should be abbreviated')])
    zip = StringField('Zip', validators=[DataRequired()])
    submit = SubmitField('Submit')

