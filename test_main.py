from paste.fixture import TestApp
from nose.tools import *
from main_app import app

class TestCode():
	def test_index(self):
		middleware = []
		testApp = TestApp(app.wsgifunc(*middleware))
		r = testApp.get('/h')
		assert_equal(r.status, 200)