from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import dump, tostring, fromstring
from app import db
from app.models import Address
import requests
import os

class AddressValidator:
    def __init__(self, form):
        self.address = {'name': form.name.data,
                        'address': form.address.data,
                        'zip': form.zip.data,
                        'city': form.city.data,
                        'state': form.state.data,
                        }

    def build_request_xml(self):
        root = Element('CityStateLookupRequest', USERID='900NA0005366')
        zip_sub = SubElement(root, 'ZipCode')
        SubElement(zip_sub, "Zip5").text =  self.address['zip']
        return tostring(root)

    def request(self, test=False):
        if test:
            response = requests.get(
                'https://secure.shippingapis.com/ShippingAPITest.dll', params={'API': 'CityStateLookup', 'XML': self.build_request_xml()})
        else:
            response = requests.get(
                'https://secure.shippingapis.com/ShippingAPI.dll', params={'API': 'CityStateLookup', 'XML': self.build_request_xml()})
        return self.parse_response(response)

    def parse_response(self, string_response):
        result = {}
        tree_response = fromstring(string_response.content)
        for child in tree_response.iter():
            if child.text:
                result[child.tag] = child.text.lower()
        return self.save_address(result)

    def determine_error(self, result):
        if 'Description' in result:
            return result['Description']
        elif (result['City'] != self.address['city'].lower()
              and result['State'] != self.address['state'].lower()):
            return 'Incorrect City & State: Did you mean {}, {}?'.format(
                self.address['city'],
                self.address['state'])
        elif result['City'] != self.address['city'].lower():
            return 'Incorrect City: Did you mean {}?'.format(
                result['City'])
        elif result['State'] != self.address['state'].lower():
            return 'Incorrect State: Did you mean {}?'.format(
                result['State'].upper())
        else:
            return None

    def save_address(self, result):
        address = Address( name = self.address['name'],
                          address = self.address['address'],
                          city = self.address['city'],
                          state = self.address['state'],
                          zip = self.address['zip'],
                          error = self.determine_error(result))
        db.session.add(address)
        db.session.commit()

