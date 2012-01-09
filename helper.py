import httpagentparser
import string
import time
import random
import datetime 
from controlers import Menu

def get_delta(date_time, period):
    delta = {}
    delta['seconds'] = datetime.timedelta(seconds = date_time.second)
    delta['minutes'] = datetime.timedelta(minutes = date_time.minute) + delta['seconds']
    delta['hours'] = datetime.timedelta(hours = date_time.hour) + delta['minutes']
    return delta[period]

def prpare_list(in_dic, out_list):
    for key,value in in_dic.items():
        element = [str(key), value]
        out_list.append(element)

def parse_user_agent(input_string):
    return httpagentparser.detect(input_string)


def _id_generator(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def prepare_date(in_date):
    return time.mktime(time.strptime(in_date,"%m/%d/%Y"))


def get_param(param_name, data):
    if param_name in data:
        return data[param_name] 
    else:
        return None

def main_menu():
    menu = Menu()
    menu.append_item('main','/')
    menu.append_item('stat','/stat')
    menu.append_item('about','/about')
    return menu.get_menu()
