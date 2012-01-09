from models import url, click
import helper
import pymongo
import time
import datetime 

class Shortener(object):
    
    def short_it(self, url_in):
        new_url = {'url' : url_in}
        code = helper._id_generator()
        size = 5
        tries = 0
        query = {'code': code}
        while url.get_url_by_key(query):
            code = helper._id_generator(size)
            tries += 1
            if tries > 100000:
                tries = 0
                size += 1
        new_url['code'] = code
        url.save_url(new_url)
        return code

    def format_url(self, url_in):
        if '://' in url_in:
            return url_in
        return 'http://' + url_in

    def get_url(self, code):
        query = {'code': code}
        return url.get_url_by_key(query)


class ClickInfo(object):

    def __init__(self):
        self.data = {}
        self.data['os'] ={}
        self.data['browser'] ={}
        self.data['time'] ={}


    def __prepare_name(self, params, category):
        if category in ['browser', 'os']:
            return params[category]['name']
        elif category in ['time']:
            return params[category]
        else:
            return ''

    def __count_param(self, params, category, period_f = None, period_p = None):
        if category in params:
            name = self.__prepare_name(params, category)
            if period_f:
                name = period_f(name, period_p)
            self.__increase_param(category, name)        
        else:
            self.__increase_param(category, 'unknown')


    def __increase_param(self, category, param):
        if param in self.data[category]:
            self.data[category][param] += 1
        else:
            self.data[category][param]= 1

    def save_click(self, web_env, path):
        click_data = {}
        click_data['refer'] = web_env.get('HTTP_REFERER', None)
        click_data['user_agent'] = helper.parse_user_agent(web_env.get('HTTP_USER_AGENT', ''))
        click_data['time'] = time.time()
        click_data['code'] = path
        click.set_click(click_data)
        return True

    def round_time(self, time_value, period):
        time_value = round(time_value)
        date_time = datetime.datetime.fromtimestamp(time_value)
        date_time = date_time - helper.get_delta(date_time, period)
        return date_time


    def count_param(self, params):
        for param in params:
            if 'user_agent' not in param:
                continue
            self.__count_param(param['user_agent'], 'os')
            self.__count_param(param['user_agent'], 'browser')
            self.__count_param(param, 'time', period_f = self.round_time, period_p = 'seconds')

    def get_click_info(self, path, **kwargs):    
        query = {'code': path}
        return_data = {}
        from_date = helper.get_param('f_date',kwargs)
        to_date = helper.get_param('t_date',kwargs)
        if from_date and to_date:
            query['time'] = {'$gte':from_date ,'$lte':to_date}
        elif from_date:
            query['time'] = {'$gte':from_date}
        elif to_date:
            query['time'] = {'$lte':to_date}
        sort = [('time', pymongo.ASCENDING)] 
        click_data = click.get_clicks(query, sort_q = sort)
        if not click_data:
            return return_data
        return_data['count'] = click_data.count()
        self.count_param(click_data)
        return_data['click_statistic'] = self.data
        return return_data


class Menu(object):

    def __init__(self):
        self.menu = []

    def append_item(self,name, link):
        item = {'name': name, 'link' : link}
        self.menu.append(item)

    def get_menu(self):
        return self.menu

class Links(object):

    def __init__(self, server_name):
        self.server_name = server_name
        self.link_dict = {}
        self.link_dict['url'] = self.server_name + ''
        self.link_dict['statistic'] = self.server_name + 'stat/'
        self.link_dict['qrcode'] = self.server_name + 'qrcode/'
        self.links = []

    def add_link(self, link, param = ''):
        if link in self.link_dict:
            new_link = {}
            new_link['link'] = link
            new_link['url'] = self.link_dict[link] + param
            self.links.append(new_link)

    def get_links(self):
        return self.links