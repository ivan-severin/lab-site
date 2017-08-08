from app import app

import unittest
import os

class BasicTestCase(unittest.TestCase):
    """Basic tests"""
    def test_index(self):
        tester =  app.test_client(self)
        response = tester.get('/', content_type='thml/text')
        self.assertEqual(response.status_code, 200)
    
    def test_database(self):
        tester = os.path.exists('app.db')
        self.assertTrue(tester)
    
    def test_css_exist(self):
        tester = os.path.exists('static/css/bootstrap.min.css')
        self.assertTrue(tester)
        tester = os.path.exists('static/css/style.css')
        self.assertTrue(tester)
        
if __name__ == '__main__':
  unittest.main()