"""
Main Test File
"""

import unittest

from app import app, db
from app.models import Address
from app.address_validator import ZipService


class AddressTestCase(unittest.TestCase):
    """ Main Test Class """

    def setUp(self):
        app.config['SQLALCHEMY_DATABAASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_multiple_addresses(self):
        """ Tests that the index shows multiple addresses"""
        test = app.test_client(self)
        address_1 = Address(name='Casa Bonita', address='6715 West Colfax Ave',
                            city='Denver', state='CO', zip='80214')
        address_2 = Address(name='Aquarium', address='700 Water Street',
                            city='Denver', state='CO', zip='80211')

        db.session.add(address_1)
        db.session.add(address_2)
        db.session.commit()

        response = test.get('/addresses', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Casa Bonita', response.data)
        self.assertIn(b'6715 West Colfax Ave', response.data)
        self.assertIn(b'Denver', response.data)
        self.assertIn(b'CO', response.data)
        self.assertIn(b'Delete', response.data)

        self.assertIn(b'Aquarium', response.data)
        self.assertIn(b'700 Water Street', response.data)
        self.assertIn(b'80211', response.data)

    def test_create_shows_a_form(self):
        """ Test that the create page shows a form"""
        test = app.test_client(self)

        response = test.get('/addresses/new', content_type='html/text')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address', response.data)
        self.assertIn(b'City', response.data)
        self.assertIn(b'State', response.data)
        self.assertIn(b'Zip', response.data)

    def test_address_validator_passes(self):
        """ Test that a correct address passes the validator"""
        data = {'name': 'Casa Bonita',
                'address': '6715 West Colfax Ave',
                'zip': '80214',
                'city': 'Denver',
                'state': 'CO'}
        validator = ZipService()
        validator.validate_address(data)

        result = Address.query.get(1)

        self.assertEqual(result.error, None)

    def test_address_validator_fails_city(self):
        """ Test that the validator will fail a wrong city"""
        data = {'name': 'Casa Bonita',
                'address': '6715 West Colfax Ave',
                'zip': '80214',
                'city': 'Salt Lake City',
                'state': 'CO'}
        validator = ZipService()
        validator.validate_address(data)

        result = Address.query.get(1)

        self.assertEqual(result.error, 'Incorrect City: Did you mean Denver?')

    def test_address_validator_fails_state(self):
        """ Test that the validator will fail a wrong state"""
        data = {'name': 'Casa Bonita',
                'address': '6715 West Colfax Ave',
                'zip': '80214',
                'city': 'Denver',
                'state': 'Utah'}
        validator = ZipService()
        validator.validate_address(data)

        result = Address.query.get(1)

        self.assertEqual(result.error, 'Incorrect State: Did you mean CO?')

    def test_validator_fails_city_and_state(self):
        """ Test that the validator will fail a wrong city and state"""
        data = {'name': 'Casa Bonita',
                'address': '6715 West Colfax Ave',
                'zip': '80214',
                'city': 'Salt Lake City',
                'state': 'Utah'}
        validator = ZipService()
        validator.validate_address(data)

        result = Address.query.get(1)

        self.assertEqual(result.error,
                         'Incorrect City & State: Did you mean Denver, CO?')

    def test_validator_can_lookup(self):
        zip = '80205'
        lookup = ZipService()
        result = lookup.perform_lookup(zip)

        self.assertEqual(result['Zip5'], zip)
        self.assertEqual(result['City'], 'Denver')
        self.assertEqual(result['State'], 'CO')


if __name__ == '__main__':
    unittest.main()
