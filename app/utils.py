import os
import random
import string
import typing
import requests


def percent_type(d: typing.Union[str, int]) -> str:
    """"""
    return '%s'
    #if type(d) is str:
    #    return '%s'
    #if type(d) is int:
    #    return '%i'


def random_string(length: int=8) -> str:
    return ''.join(random.choices(string.hexdigits, k=length))


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    try:
        requests.get(host + "/index")
        return True
    except:
        return False

def get_central_ip():
    # TODO: get central IP from config file.
    return "http://192.168.2.8:5000"

def get_data_ip(username):
    central_ip = get_central_ip()
    response = requests.get(central_ip + "/api/user/address?username=" + username)

    if response.json()['data']['address']:
        return response.json()['data']['address']
    else:
        return False