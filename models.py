from settings import DB


class Url(object):

	def __init__(self):
		self.urls = DB.urls

	def get_Urls(self):	
		return self.urls.find()

	def get_url_by_key(self, key_name, key_value):
		return self.urls.find_one({key_name : key_value})

	def save_url(self, url):
		self.urls.save(url)
		return True

class Click(object):

	def __init__(self):
		self.clicks = DB.clicks

	def set_click(self, params):
		self.clicks.save(params)
		return True

	def get_clicks(self, query):
		return self.clicks.find(query)
		