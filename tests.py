from app import app

import unittest
import os

class BasicTestCase(unittest.TestCase):
    """Basic Ping tests"""
    def test_index(self):
        tester =  app.test_client(self)
        response = tester.get('/', content_type='thml/text')
        self.assertEqual(response.status_code, 200)

    def test_news(self):
        tester =  app.test_client(self)
        response = tester.get('/news/', content_type='thml/text')
        self.assertEqual(response.status_code, 200)

    def test_publications(self):
        tester =  app.test_client(self)
        response = tester.get('/publications/', content_type='thml/text')
        self.assertEqual(response.status_code, 200)
    
    def test_contacts(self):
        tester =  app.test_client(self)
        response = tester.get('/contacts/', content_type='thml/text')
        self.assertEqual(response.status_code, 200)
    
    def test_about(self):
        tester =  app.test_client(self)
        response = tester.get('/about/', content_type='thml/text')
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