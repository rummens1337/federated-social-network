import os
import random
import string
import typing
import requests
import json
import flask


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
    return flask.request.url_root

def get_data_ip(username):
    response = requests.get(get_central_ip() + "/api/user/address?username=" + username)

    if response.json()['data']['address']:
        return response.json()['data']['address']
    else:
        return False