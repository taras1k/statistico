import httpagentparser
from models import Url, Click
import string
import time
import random
import web
import re

def format_url(url):
    r = re.compile(r'://')
    res = r.match(url)
    if res:
        return url
    return 'http://' + url


def parse_user_agent(input_string):
    return httpagentparser.detect(input_string)


def _id_generator(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def _count_param(params, category, data):
    if category in params:
            name = params[category]['name']
            if name not in data[category]:
                data[category][name] = 1
            else: 
                data[category][name] += 1

def count_param(params):
    data = {}
    data['os'] ={}
    data['browser'] ={}
    for param in params:
        if 'user_agent' not in param:
            continue
        _count_param(param['user_agent'], 'os', data)
        _count_param(param['user_agent'], 'browser', data)
    return data


def get_click_info(path):
    click = Click()
    data = {}
    query = {'code': path}
    click_data = click.get_clicks(query)
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