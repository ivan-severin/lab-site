from app import app



from app.database import  db_session, init_db
from app.models import User, Role
from flask_security import Security, SQLAlchemyUserDatastore

import unittest
import os

# class BasicTestCase(unittest.TestCase):
#     """Basic Ping tests"""
#     def test_index(self):
#         tester =  app.test_client(self)
#         response = tester.get('/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)

#     def test_news(self):
#         tester =  app.test_client(self)
#         response = tester.get('/news/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)

#     def test_publications(self):
#         tester =  app.test_client(self)
#         response = tester.get('/publications/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
    
#     def test_contacts(self):
#         tester =  app.test_client(self)
#         response = tester.get('/contacts/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
    
#     def test_about(self):
#         tester =  app.test_client(self)
#         response = tester.get('/about/', content_type='html/text')
#         self.assertEqual(response.status_code, 200)
    
    
#     def test_database(self):
#         tester = os.path.exists('app.db')
#         self.assertTrue(tester)
    
#     def test_css_exist(self):
#         tester = os.path.exists('static/css/bootstrap.min.css')
#         self.assertTrue(tester)
#         tester = os.path.exists('static/css/style.css')
#         self.assertTrue(tester)


class TestUser(unittest.TestCase):
    """docstring for TestUser"""
    def setUp(self):
        pass
        # app.config.from_object('config')
        # Initialize the SQLAlchemy data store and Flask-Security.
        

    def testCreate(self):
        
        init_db()
        user_datastore = SQLAlchemyUserDatastore(db_session, User, Role)
        security = Security(app, user_datastore)

        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='end-user', description='End user')
        db_session.commit()

if __name__ == '__main__':
  unittest.main()