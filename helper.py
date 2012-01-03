import httpagentparser
from models import Url, Click
import string
import time
import random
import web
import re
import datetime 
import pymongo

def __get_delta(date_time, period):
    delta = {}
    delta['seconds'] = datetime.timedelta(seconds = date_time.second)
    delta['minutes'] = datetime.timedelta(minutes = date_time.minute) + delta['seconds']
    delta['hours'] = datetime.timedelta(hours = date_time.hour) + delta['minutes']
    return delta[period]

def round_time(time_value, period):
    time_value = round(time_value)
    date_time = datetime.datetime.fromtimestamp(time_value)
    date_time = date_time - __get_delta(date_time, period)
    return date_time

def format_url(url):
    r = re.compile(r'://')
    res = r.match(url)
    if res:
        return url
    return 'http://' + url

def prpare_list(in_dic, out_list):
    for key,value in in_dic.items():
        element = [str(key), value]
        out_list.append(element)


def parse_user_agent(input_string):
    return httpagentparser.detect(input_string)


def _id_generator(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def __prepare_name(params, category):
    if category in ['browser', 'os']:
        return params[category]['name']
    elif category in ['time']:
        return params[category]
    else:
        return ''

def _count_param(params, category, data, period_f = None, period_p = None):
    if category in params:
        name = __prepare_name(params, category)
        if period_f:
            name = period_f(name, period_p)
        if name not in data[category]:
            data[category][name] = 1
        else: 
            data[category][name] += 1


def count_param(params):
    data = {}
    data['os'] ={}
    data['browser'] ={}
    data['time'] ={}
    for param in params:
        if 'user_agent' not in param:
            continue
        _count_param(param['user_agent'], 'os', data)
        _count_param(param['user_agent'], 'browser', data)
        _count_param(param, 'time', data, period_f = round_time, period_p = 'seconds')
    return data


def get_click_info(path):
    click = Click()
    data = {}
    query = {'code': path}
    sort = [('time', pymongo.DESCENDING)]
    click_data = click.get_clicks(query, sort_q = sort)
    if not click_data:
        return data
    data['count'] = click_data.count()
    data['env'] = count_param(click_data)
    return data

    
def short_it(url):
    url_models = Url()
    url_model = {'url' : url}
    code = _id_generator()
    size = 5
    tries = 0
    while url_models.get_url_by_key('code', code):
        code = _id_generator(size)
        tries += 1
        if tries > 100000:
            tries = 0
            size += 1
    url_model['code'] = code
    url_models.save_url(url_model)
    return code
        
def save_click(web_env, path):
    click = Click()
    click_data = {}
    click_data['refer'] = web_env.get('HTTP_REFERER', None)
    click_data['user_agent'] = parse_user_agent(web_env.get('HTTP_USER_AGENT', ''))
    click_data['time'] = time.time()
    click_data['code'] = path
    click.set_click(click_data)
    return True
