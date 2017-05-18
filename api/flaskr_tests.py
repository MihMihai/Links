import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])
		
	def signup(self,email,name,password,birth_day,birth_month,birth_year):
		return self.app.post('/api/signup',data=dict(
			email=email,
			name=name,
			password=password,
			birth_day=birth_day,
			birth_month=birth_month
			birth_year=birth_year))
			
	def test_signup(self):
		rv = self.signup('test@qwerty.com','Test','12345','26','May','1999')
		assert dict(status=ok) in rv.data

if __name__ == '__main__':
    unittest.main()