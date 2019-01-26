from app import app

import unittest

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        test = app.test_client(self)
        response = test.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'TRELORA')


if __name__ == '__main__':
    unittest.main()
