""" Validates correct City and State using USPS API"""
from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import tostring, fromstring

import os
import requests

from app import db
from app.models import Address


class ZipService:
    """ Validates correct City and State using USPS API"""

    def perform_lookup(self, zip):
        """ Looks up city/state for zip """
        self.address = {}
        self.address['zip'] = zip
        response = self.request()
        if 'Description' in response:
            return response
        return self.format_response(response)

    def validate_address(self, data):
        self.address = data
        result = self.request()
        self.save_address(result)

    def format_response(self, response):
        response['City'] = response['City'].capitalize()
        response['State'] = response['State'].upper()
        return response

    def build_request_xml(self):
        """ Build the XML for the API Request """
        root = Element('CityStateLookupRequest',
                       USERID=os.environ.get('USPS_KEY'))
        zip_sub = SubElement(root, 'ZipCode')
        SubElement(zip_sub, "Zip5").text = self.address['zip']
        return tostring(root)

    def request(self):
        """ Executes the request against USPS """
        response = requests.get(
            'https://secure.shippingapis.com/ShippingAPI.dll',
            params={'API': 'CityStateLookup', 'XML': self.build_request_xml()})
        return self.parse_response(response)

    def parse_response(self, string_response):
        """ Parses the returned XML response into a dictionary """
        result = {}
        tree_response = fromstring(string_response.content)
        for child in tree_response.iter():
            if child.text:
                result[child.tag] = child.text.lower()
        return result

    def determine_error(self, result):
        """ Checks if the supplied city/state match the API response """
        if 'Description' in result:
            return result['Description']
        elif (result['City'] != self.address['city'].lower()
              and result['State'] != self.address['state'].lower()):
            return 'Incorrect City & State: Did you mean {}, {}?'.format(
                result['City'].capitalize(),
                result['State'].upper())
        elif result['City'] != self.address['city'].lower():
            return 'Incorrect City: Did you mean {}?'.format(
                result['City'].capitalize())
        elif result['State'] != self.address['state'].lower():
            return 'Incorrect State: Did you mean {}?'.format(
                result['State'].upper())

    def save_address(self, result):
        """ Saves the address to the DB """
        address = Address(name=self.address['name'],
                          address=self.address['address'],
                          city=self.address['city'],
                          state=self.address['state'],
                          zip=self.address['zip'],
                          error=self.determine_error(result))
        db.session.add(address)
        db.session.commit()
