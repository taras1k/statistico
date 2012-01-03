from settings import DB


class Url(object):

    def __init__(self):
        self.urls = DB.urls

    def get_Urls(self): 
        return self.urls.find()

    def get_url_by_key(self, query):
        return self.urls.find_one(query)

    def save_url(self, url):
        self.urls.save(url)
        return True

class Click(object):

    def __init__(self):
        self.clicks = DB.clicks

    def set_click(self, params):
        self.clicks.save(params)
        return True

    def get_clicks(self, query, sort_q = None):
        if sort_q:
            return self.clicks.find(query, sort = sort_q)
        else: 
            return self.clicks.find(query)
        